import pdfplumber
import pandas as pd
from datetime import datetime
from utils.database import Appointment, Session

class DataIngestionAgent:
    def __init__(self, data_dir="data/"):
        self.data_dir = data_dir

    def _extract_date_from_pdf(self, pdf_path):
        """Extracts appointment date from the pdf"""
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            for line in text.split("\n"):
                if line.lower().startswith("appointment date:"):
                    date_part = line.split(":", 1)[1].strip().split(",")[0].strip()
                    year = datetime.now().year
                    return datetime.strptime(f"{date_part} {year}", "%d %B %Y").date()
        return None


    def _extract_appointments_from_pdf(self, pdf_path):
        """Extracts appointment data from a PDF."""
        appointments = []
        date = self._extract_date_from_pdf(pdf_path)
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    for index, row in df.iterrows():
                        sl = row.get('SL', None)
                        if not sl or not str(sl).isdigit():
                           print(f"Error skipping row with invalid SL {sl}, row: {row}")
                           continue
                        try:
                            sl = int(sl)
                            appointment_time_str = f"{date.strftime('%Y-%m-%d')} 00:00"
                            appointment_time = datetime.strptime(appointment_time_str, "%Y-%m-%d %H:%M")

                            age = row.get("Age", None)
                            if age:
                              try:
                                  age = int(age)
                              except:
                                  age = None
                            else:
                                age = None

                            if row.get("Patient Name", None) and row.get("Phone", None):
                                 appointments.append({
                                     "patient_name": row["Patient Name"],
                                     "age": age,
                                     "sex": row.get("Sex", None),
                                     "phone": row["Phone"],
                                     "type": row.get("Type", None),
                                     "category": row.get("Category", None),
                                     "appointment_time": appointment_time,
                                     "check_in_time": None,
                                     "priority_score": 0,
                                     "sl": sl
                                 })
                        except Exception as e:
                            print(f"Error extracting appointment: {e}, row: {row}")
        return appointments

    def ingest_data(self, pdf_path):
        """Loads appointments from the pdf to the database"""
        appointments = self._extract_appointments_from_pdf(pdf_path)
        session = Session()
        try:
            for appt_data in appointments:
                 appointment = Appointment(
                    patient_name = appt_data.get("patient_name"),
                    age = appt_data.get("age"),
                    sex = appt_data.get("sex"),
                    phone = appt_data.get("phone"),
                    appointment_time = appt_data.get("appointment_time"),
                    type = appt_data.get("type"),
                    category = appt_data.get("category"),
                    check_in_time = appt_data.get("check_in_time"),
                    is_checked_in = False,
                    priority_score = appt_data.get("priority_score"),
                    is_completed = False,
                    sl = appt_data.get("sl")
                 )
                 session.add(appointment)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error inserting data: {e}")
        finally:
            session.close()