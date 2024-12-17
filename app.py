import streamlit as st
from agents.data_ingestion_agent import DataIngestionAgent
from agents.feature_extraction_agent import FeatureExtractionAgent
from agents.priority_calculation_agent import PriorityCalculationAgent
from agents.priority_queue_management_agent import PriorityQueueManagementAgent
from agents.real_time_monitoring_agent import RealTimeMonitoringAgent
from utils.database import Appointment, Session, Base, engine
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from datetime import datetime
from dotenv import load_dotenv
import os
import json

load_dotenv()

def main():
    st.title("Physician Chamber Appointment System")

    # Initialize agents
    ingestion_agent = DataIngestionAgent()
    feature_agent = FeatureExtractionAgent()
    priority_calc_agent = PriorityCalculationAgent()
    queue_agent = PriorityQueueManagementAgent()
    monitoring_agent = RealTimeMonitoringAgent()

    # Initialize Session state for queue
    if "queue" not in st.session_state:
        st.session_state.queue = []

    def clear_database():
        """Clears all data from the database."""
        session = Session()
        try:
            session.query(Appointment).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error clearing database: {e}")
        finally:
            session.close()


    # Function to load data from PDF
    def load_appointments():
        uploaded_file = st.file_uploader("Upload your PDF here", type=["pdf"])
        if uploaded_file is not None:
            try:
                with open("temp.pdf", "wb") as f:
                   f.write(uploaded_file.read())
                clear_database()
                ingestion_agent.ingest_data('temp.pdf')
                st.success("Appointments loaded successfully!")
                st.session_state.queue = queue_agent.get_prioritized_queue()
                st.rerun()
            except Exception as e:
                 st.error(f"Error loading appointments: {e}")




    # load appointments from pdf if the queue is empty.
    if not st.session_state.queue:
        load_appointments()


    # Load the queue from database if it exists in session state.
    if st.session_state.queue:
          # Convert queue to dataframe
          df = pd.DataFrame([{"id": appt.id,
                             "patient_name": appt.patient_name,
                             "type": appt.type,
                             "check_in_time": appt.check_in_time,
                             "priority_score": appt.priority_score,
                             "sl": appt.sl,
                             "is_checked_in": appt.is_checked_in
                            } for appt in st.session_state.queue])
          # Check in functionality
          def check_in_patient(patient_id):
               monitoring_agent.check_in(patient_id)
               priority_calc_agent.update_priority_in_db(patient_id)
               st.session_state.queue = queue_agent.get_prioritized_queue()
               st.rerun()


          def mark_appointment_done(patient_id):
                session = Session()
                try:
                    appointment = session.query(Appointment).filter(Appointment.id == patient_id).first()
                    if appointment:
                        appointment.is_completed = True
                        session.commit()
                        st.session_state.queue = queue_agent.get_prioritized_queue()
                        st.rerun()
                except Exception as e:
                    session.rollback()
                    print(f"Error marking the appointment complete {e}")
                finally:
                    session.close()

          # Build the ag grid
          gb = GridOptionsBuilder.from_dataframe(df)
          gb.configure_selection(selection_mode="single", use_checkbox=False)
          gb.configure_column("id", editable=False)
          gb.configure_column("patient_name", editable=False)
          gb.configure_column("type", editable=False)
          gb.configure_column("priority_score", editable=False)
          gb.configure_column("sl", editable = False)
          gb.configure_column("check_in_time", editable = False)
          gb.configure_column("is_checked_in", editable = False)
          gb.configure_column("check_in_time", cellStyle={'font-style': 'italic'})


          # If the patient is checked in, we make the cell green
          for i in range(len(df)):
            if df['is_checked_in'][i]:
                gb.configure_column("patient_name", cellStyle = JsCode(
                    """
                    function(params) {
                         return {'backgroundColor': 'green'}
                    };
                    """
                ))

          gb.configure_column(
              "check_in",
              headerName="Check In",
              cellRenderer=JsCode("""
                  function(params) {
                      return '<button id="check_in_' + params.data.id + '">Check In</button>';
                 }
             """),
             width=120
          )

          gb.configure_column(
              "done",
              headerName="Done",
              cellRenderer=JsCode("""
                  function(params) {
                      return '<button id="done_' + params.data.id + '">Done</button>';
                  }
              """),
              width=100
          )

          go = gb.build()
          go["allow_unsafe_jscode"] = True
          go["suppressMoveWhenRowDragging"] = True

          # Create custom JsCode for onGridReady event
          on_grid_ready = JsCode(
              """
                function(params) {
                  var grid = params.api;
                   function checkIn(e){
                       grid.applyTransaction({
                           add:[],
                           update:[],
                           remove: []
                       })
                        // Send a message to streamlit
                        // The message will be handled by a callback on the python side.
                        Streamlit.setComponentValue(e.id)
                    }
                   function done(e){
                        grid.applyTransaction({
                           add:[],
                           update:[],
                           remove: []
                       })
                        // Send a message to streamlit
                        // The message will be handled by a callback on the python side.
                        Streamlit.setComponentValue(e.id + "_done")
                    }
                     params.api.addEventListener('rowDragEnd', function(event) {
                            var rowsToUpdate = [];
                            params.api.forEachNodeAfterFilterAndSort( function(rowNode, index) {
                              rowsToUpdate.push({id: rowNode.data.id, sl: index+1});
                            });
                            Streamlit.setComponentValue(JSON.stringify(rowsToUpdate));
                        });
                   window.checkIn = checkIn;
                   window.done = done;
                };
                """
          )


          grid_response = AgGrid(df,
                                  gridOptions=go,
                                  data_return_mode='AS_INPUT',
                                  update_mode='MODEL_CHANGED',
                                  fit_columns_on_grid_load=True,
                                  theme='streamlit', #Add theme color to the table
                                  enable_enterprise_modules=True,
                                  height=350,
                                  width='100%',
                                  reload_data=True,
                                  allow_unsafe_jscode=True,
                                  on_grid_ready=on_grid_ready,
                                  key = "grid_table"

                                  )

          # Handle button press event
          if grid_response.get('data') is not None and not grid_response.get('data').empty:
           selected_value = st.session_state.get("agGrid_key", None)
           if selected_value:
              if str(selected_value).endswith("_done"):
                mark_appointment_done(int(selected_value.replace("_done", "")))
              else:
                check_in_patient(int(selected_value))
              st.session_state["agGrid_key"] = None # Remove key from session state
          if grid_response.get('data_rows'):
            selected_rows = grid_response.get('data_rows', [])
            if selected_rows:
                session = Session()
                try:
                    rowsToUpdate = st.session_state.get("agGrid_key", None)
                    if rowsToUpdate:
                        rowsToUpdate =  json.loads(rowsToUpdate)
                        for row in rowsToUpdate:
                            appt = session.query(Appointment).filter(Appointment.id == row['id']).first()
                            if appt:
                                appt.sl = row['sl']
                            session.commit()
                            st.session_state.queue = queue_agent.get_prioritized_queue()
                            st.session_state["agGrid_key"] = None # Remove key from session state
                            st.rerun()
                finally:
                   session.close()

if __name__ == "__main__":
    main()
