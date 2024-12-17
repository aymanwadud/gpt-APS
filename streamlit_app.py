import streamlit as st
from agents.data_ingestion_agent import DataIngestionAgent
from agents.feature_extraction_agent import FeatureExtractionAgent
from agents.priority_calculation_agent import PriorityCalculationAgent
from agents.priority_queue_management_agent import PriorityQueueManagementAgent
from agents.real_time_monitoring_agent import RealTimeMonitoringAgent
from utils.database import Appointment, Session

def main():
    st.title("Physician Chamber Appointment Prioritization System")

    # Initialize agents
    ingestion_agent = DataIngestionAgent()
    feature_agent = FeatureExtractionAgent()
    priority_calc_agent = PriorityCalculationAgent()
    queue_agent = PriorityQueueManagementAgent()
    monitoring_agent = RealTimeMonitoringAgent()

    # Load data from PDF (button)
    if st.button("Load Appointments from PDF"):
        ingestion_agent.ingest_data('test_schedule.pdf')
        st.success("Appointments loaded to DB!")

    # Display the prioritized queue
    st.header("Prioritized Appointment Queue")
    queue = queue_agent.get_prioritized_queue()

    if queue:
      for appt in queue:
          st.write(f"- {appt.patient_name} (Type: {appt.type}, Priority Score: {appt.priority_score})")
    else:
       st.write("No Appointments in the queue.")

    # Check-in the first patient (button)
    if queue and st.button("Check-in First Patient"):
       session = Session()
       try:
           appt_to_checkin = session.query(Appointment).order_by(Appointment.sl).first()
           if appt_to_checkin:
              st.write(f"Checking in: {appt_to_checkin.patient_name}")
              check_in_time = monitoring_agent.check_in(appt_to_checkin.id)
              st.write(f"Check-in time for {appt_to_checkin.patient_name}: {check_in_time}")
              priority_calc_agent.update_priority_in_db(appt_to_checkin.id)
              st.experimental_rerun() # Rerun to update the queue after check in
           else:
               st.error("No Appointment to check in.")
       finally:
          session.close()

if __name__ == "__main__":
    main()