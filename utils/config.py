import os
from datetime import timedelta

WORKING_HOURS = ["09:00", "17:00"]
APPOINTMENT_DURATION = timedelta(minutes=30)
PRIORITY_FACTORS = {"fever": 10, "emergency": 20, "headache": 5}

# Construct the database URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
  DATABASE_URL = "sqlite:///./appointments.db" # Default URL