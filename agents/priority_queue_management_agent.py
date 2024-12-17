from utils.database import Appointment, Session
import copy
class PriorityQueueManagementAgent:
    def get_prioritized_queue(self):
        """Returns the prioritized queue (appointments sorted by priority)."""
        session = Session()
        try:
          all_appointments = session.query(Appointment).filter(Appointment.is_completed == False).order_by(Appointment.priority_score.desc(), Appointment.sl).all()
          return [copy.copy(appt) for appt in all_appointments]
        finally:
           session.close()