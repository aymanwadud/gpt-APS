import datetime
from utils.database import Appointment, Session

class RealTimeMonitoringAgent:
    def check_in(self, appointment_id):
        session = Session()
        try:
            appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
            if appointment:
               appointment.check_in_time = datetime.datetime.now()
               appointment.is_checked_in = True
               session.commit()
               return appointment.check_in_time
            return None
        except Exception as e:
           session.rollback()
           print(f"Error during check in {e}")
        finally:
           session.close()

    def get_check_in_time(self, appointment_id):
        session = Session()
        try:
          appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
          if appointment:
             return appointment.check_in_time
          return None
        finally:
            session.close()