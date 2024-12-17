import pdfplumber
import pandas as pd
from datetime import datetime
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from utils.config import OPENAI_API_KEY
import uuid
import os


class DataIngestionAgent:
    def init(self, data_dir="data/"):
        self.data_dir = data_dir
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.vector_db = Chroma(persist_directory=os.path.join(data_dir, "chroma_db"), embedding_function=self.embeddings)

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
                            if row.get("Patient Name", None) and row.get("Phone", None):
                                 appointments.append({
                                     "patient_name": row["Patient Name"],
                                     "age": row.get("Age", None),
                                     "sex": row.get("Sex", None),
                                     "phone": row["Phone"],
                                     "type": row.get("Type", None),
                                     "category": row.get("Category", None),
                                     "appointment_time": appointment_time,
                                     "check_in_time": None,
                                     "priority_score": 0,
                                     "sl": sl,
                                      "id": str(uuid.uuid4())
                                 })
                        except Exception as e:
                            print(f"Error extracting appointment: {e}, row: {row}")
        return appointments
    
    def ingest_data(self, pdf_path):
        """Loads appointments from the pdf to the database"""
        appointments = self._extract_appointments_from_pdf(pdf_path)
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        for appt_data in appointments:
           texts = text_splitter.split_text(f"Patient Name: {appt_data['patient_name']}. Type: {appt_data['type']}. Category: {appt_data['category']}")
           self.vector_db.add_texts(texts, ids=[appt_data['id']])
        return appointments
