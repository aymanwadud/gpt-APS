# utils/database.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
# Removed the DATABASE_URL import since we are not using postgres
Base = declarative_base()


class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, Sequence('appointment_id_seq'), primary_key=True)
    patient_name = Column(String)
    age = Column(Integer, nullable = True)
    sex = Column(String)
    phone = Column(String)
    appointment_time = Column(DateTime)
    type = Column(String)
    category = Column(String)
    check_in_time = Column(DateTime, nullable=True)
    is_checked_in = Column(Boolean, default=False)
    priority_score = Column(Float, default = 0.0)
    is_completed = Column(Boolean, default = False)
    sl = Column(Integer, nullable = False)


# Removed the usage of the engine and session here
# engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
