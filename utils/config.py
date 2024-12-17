import os
from datetime import timedelta

WORKING_HOURS = ["09:00", "17:00"]
APPOINTMENT_DURATION = timedelta(minutes=30)
PRIORITY_FACTORS = {"fever": 10, "emergency": 20, "headache": 5}

# Construct the database URL from environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
  raise ValueError("OPENAI_API_KEY environment variable not set!")
