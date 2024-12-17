from utils.database import Appointment, Session

class FeatureExtractionAgent:
    def extract_features(self, appointment_id):
        session = Session()
        try:
           appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
           if appointment:
            return {
                "reason": appointment.type,
                "check_in_time": appointment.check_in_time,
                "priority_score": appointment.priority_score,
                "sl": appointment.sl,
                "id": appointment.id
            }
           return None
        finally:
            session.close()