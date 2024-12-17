# main.py
from agents.data_ingestion_agent import DataIngestionAgent
from agents.feature_extraction_agent import FeatureExtractionAgent
from agents.priority_calculation_agent import PriorityCalculationAgent
from agents.priority_queue_management_agent import PriorityQueueManagementAgent
from agents.real_time_monitoring_agent import RealTimeMonitoringAgent
from utils.config import DATA_DIR
import datetime


def main():
    # Initialize agents
    ingestion_agent = DataIngestionAgent(data_dir=DATA_DIR)
    feature_agent = FeatureExtractionAgent()
    priority_calc_agent = PriorityCalculationAgent()
    queue_agent = PriorityQueueManagementAgent()
    monitoring_agent = RealTimeMonitoringAgent()

    # Load data
    appointments = ingestion_agent.ingest_data(DATA_DIR + 'appointments_2024-08-22.json')
    print("Loaded Appointments: ", appointments)

    for appt in appointments:
      features = feature_agent.extract_features(appt)
      priority_score = priority_calc_agent.calculate_priority(features)
      queue_agent.add_appointment(appt, priority_score)
    print("Initial Priority Queue: ", queue_agent.get_prioritized_queue())

    # Let us simulate check in
    appt_to_checkin = appointments[0]
    check_in_time = monitoring_agent.check_in(appt_to_checkin)
    print(f"Check in time for {appt_to_checkin.get('appointment_id')} : ", check_in_time)
    appt_to_checkin['check_in_time'] = check_in_time
    features = feature_agent.extract_features(appt_to_checkin)
    priority_score = priority_calc_agent.calculate_priority(features)
    queue_agent.update_priority(appt_to_checkin, priority_score)
    print("Updated Priority Queue: ", queue_agent.get_prioritized_queue())

if __name__ == "__main__":
    main()