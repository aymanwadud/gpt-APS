from agents.data_ingestion_agent import DataIngestionAgent
from agents.feature_extraction_agent import FeatureExtractionAgent
from agents.priority_calculation_agent import PriorityCalculationAgent
from agents.priority_queue_management_agent import PriorityQueueManagementAgent
from agents.real_time_monitoring_agent import RealTimeMonitoringAgent
from utils.database import Appointment, Session


def main():
    # Initialize agents
    ingestion_agent = DataIngestionAgent()
    feature_agent = FeatureExtractionAgent()
    priority_calc_agent = PriorityCalculationAgent()
    queue_agent = PriorityQueueManagementAgent()
    monitoring_agent = RealTimeMonitoringAgent()

    # Load data from PDF
    ingestion_agent.ingest_data('test_schedule.pdf')
    print("Appointments loaded to DB")

    # Get initial priority queue
    print("Initial Priority Queue: ", queue_agent.get_prioritized_queue())


    # Simulate check-in
    session = Session()
    try:
       appt_to_checkin = session.query(Appointment).order_by(Appointment.sl).first()
       if appt_to_checkin:
            print(f"Checking in: {appt_to_checkin.patient_name}")
            check_in_time = monitoring_agent.check_in(appt_to_checkin.id)
            print(f"Check-in time for {appt_to_checkin.patient_name}: {check_in_time}")
            priority_calc_agent.update_priority_in_db(appt_to_checkin.id)
            print("Updated Priority Queue: ", queue_agent.get_prioritized_queue())
       else:
           print("No appointments in the database.")

    finally:
        session.close()


if __name__ == "__main__":
    main()