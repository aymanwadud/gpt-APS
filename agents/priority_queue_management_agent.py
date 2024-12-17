# agents/priority_queue_management_agent.py

import heapq

class PriorityQueueManagementAgent:
    def __init__(self):
       self.priority_queue = []

    def add_appointment(self, appointment, priority_score):
        """Adds an appointment to the priority queue."""
        heapq.heappush(self.priority_queue, (-priority_score, appointment))

    def update_priority(self, appointment, priority_score):
       """Updates the priority score of an appointment"""
       for i, (score, appt) in enumerate(self.priority_queue):
          if appt == appointment:
            self.priority_queue[i] = (-priority_score, appt)
            heapq.heapify(self.priority_queue)
            return
       self.add_appointment(appointment, priority_score)

    def get_prioritized_queue(self):
        """Returns the prioritized queue (appointments sorted by priority)."""
        return [appt for _, appt in self.priority_queue]


if __name__ == '__main__':
    agent = PriorityQueueManagementAgent()
    agent.add_appointment({"id": 1, "name": "A"}, 10)
    agent.add_appointment({"id": 2, "name": "B"}, 5)
    agent.add_appointment({"id": 3, "name": "C"}, 15)
    print("Initial Queue: ", agent.get_prioritized_queue())
    agent.update_priority({"id": 2, "name": "B"}, 20)
    print("Queue after update: ", agent.get_prioritized_queue())