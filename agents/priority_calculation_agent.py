import datetime
from utils.database import Appointment, Session

class PriorityCalculationAgent:
    def calculate_priority(self, appointment_id):
        session = Session()
        try:
            appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
            if appointment:
                priority_score = 0.0
                if appointment.is_checked_in and appointment.check_in_time:
                   wait_time = (datetime.datetime.now() - appointment.check_in_time).total_seconds()
                   priority_score += wait_time * 0.1

                if appointment.type == "Report":
                  priority_score += 10

                return priority_score
            return None
        finally:
            session.close()

    def update_priority_in_db(self, appointment_id):
        session = Session()
        try:
            appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
            if appointment:
               appointment.priority_score = self.calculate_priority(appointment_id)
               session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error updating priority score {e}")
        finally:
           session.close()