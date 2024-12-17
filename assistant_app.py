import streamlit as st
from agents.feature_extraction_agent import FeatureExtractionAgent
from agents.priority_calculation_agent import PriorityCalculationAgent
from agents.priority_queue_management_agent import PriorityQueueManagementAgent
from agents.real_time_monitoring_agent import RealTimeMonitoringAgent
from utils.database import Appointment, Session
from datetime import datetime
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import copy
from dotenv import load_dotenv
import os
load_dotenv()

def main():
    st.title("Assistant/Doctor Appointment Queue")
    port = os.getenv("ASSISTANT_PORT", "8502")

    # Initialize agents
    feature_agent = FeatureExtractionAgent()
    priority_calc_agent = PriorityCalculationAgent()
    queue_agent = PriorityQueueManagementAgent()
    monitoring_agent = RealTimeMonitoringAgent()

    # Get Prioritized queue
    queue = queue_agent.get_prioritized_queue()

    if not queue:
      st.write("No appointments to show")
      return

    # Convert queue to dataframe
    df = pd.DataFrame([{"id": appt.id,
                         "patient_name": appt.patient_name,
                         "type": appt.type,
                         "check_in_time": appt.check_in_time,
                         "priority_score": appt.priority_score,
                         "sl": appt.sl,
                         "is_checked_in": appt.is_checked_in
                        } for appt in queue])
    # Check in functionality
    def check_in_patient(patient_id):
       check_in_time = monitoring_agent.check_in(patient_id)
       priority_calc_agent.update_priority_in_db(patient_id)
       st.experimental_rerun()

    # Build the ag grid
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode="single", use_checkbox=True)
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
    go = gb.build()

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
                            allow_unsafe_jscode = True
                            )

    # Check in button
    selected_rows = grid_response['selected_rows']
    if selected_rows:
       selected_row = selected_rows[0]
       if st.button("Check In Selected Patient"):
          check_in_patient(selected_row.get("id"))


if __name__ == "__main__":
    main()