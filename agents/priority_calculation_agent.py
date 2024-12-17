# agents/priority_calculation_agent.py
import datetime
class PriorityCalculationAgent:
    def calculate_priority(self, features):
        priority_score = 0.0

        # Rule-based priority: More wait time means higher priority
        if features.get("check_in_time"):
           wait_time = (datetime.datetime.now() - features["check_in_time"]).total_seconds()
           priority_score += wait_time * 0.1

        # Weighted factor: Checkup or report have medium priority
        if "checkup" in features.get("reason", "").lower() or "report" in features.get("reason", "").lower():
           priority_score += 10

        # Emergency is higher priority
        if "emergency" in features.get("reason", "").lower():
            priority_score += 20

        return priority_score


if __name__ == '__main__':
    agent = PriorityCalculationAgent()
    features = {"reason": "Emergency", "check_in_time": datetime.datetime.now() - datetime.timedelta(seconds = 100)}
    priority = agent.calculate_priority(features)
    print(priority)