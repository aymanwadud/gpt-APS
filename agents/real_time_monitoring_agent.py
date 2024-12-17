# agents/real_time_monitoring_agent.py
import datetime

class RealTimeMonitoringAgent:
    def __init__(self):
        self.checked_in = {}

    def check_in(self, appointment):
        self.checked_in[appointment.get("appointment_id")] = datetime.datetime.now()
        return self.checked_in[appointment.get("appointment_id")]

    def get_check_in_time(self, appointment):
        return self.checked_in.get(appointment.get("appointment_id"), None)

if __name__ == '__main__':
    agent = RealTimeMonitoringAgent()
    check_in_time = agent.check_in({"appointment_id": "1"})
    print(check_in_time)
    time = agent.get_check_in_time({"appointment_id": "1"})
    print(time)
    