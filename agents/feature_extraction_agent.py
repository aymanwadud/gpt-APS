# agents/feature_extraction_agent.py

class FeatureExtractionAgent:
    def extract_features(self, appointment):
       features = {
            "appointment_time": appointment.get("appointment_time"),
            "reason": appointment.get("reason"),
            "check_in_time": appointment.get("check_in_time"),
            "priority_score": appointment.get("priority_score")
        }
       return features

if __name__ == '__main__':
    agent = FeatureExtractionAgent()
    features = agent.extract_features({"appointment_time": "2024-08-22 10:00", "reason": "Regular checkup", "priority_score": 0})
    print(features)