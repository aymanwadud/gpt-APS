# agents/data_ingestion_agent.py

import json
from datetime import datetime

class DataIngestionAgent:
    def __init__(self, data_dir="data/"):
        self.data_dir = data_dir

    def load_data_from_json(self, filename):
        """Load data from a JSON file"""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"Error loading data from {filename}: {e}")
            return []

    def extract_appointments(self, data):
        """Extract and structure appointment data."""
        appointments = []
        for item in data:
            try:
               appointments.append({
                    "appointment_id": item.get("appointment_id", None),
                    "patient_id": item.get("patient_id", None),
                    "physician_id": item.get("physician_id", None),
                    "appointment_time": datetime.strptime(item["date"] + " " + item["time"], "%Y-%m-%d %H:%M") if item.get("date", None) and item.get("time", None) else None,
                    "reason": item.get("reason", None),
                    "check_in_time": None,
                    "priority_score": 0
               })
            except:
                print(f"Error parsing item: {item}")
                continue
        return appointments

    def ingest_data(self, filename):
        data = self.load_data_from_json(filename)
        appointments = self.extract_appointments(data)
        return appointments

if __name__ == '__main__':
    agent = DataIngestionAgent()
    app_data = agent.ingest_data('data/appointments_2024-08-22.json')
    print(app_data)