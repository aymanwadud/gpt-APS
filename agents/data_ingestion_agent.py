import pdfplumber
import pandas as pd
from datetime import datetime
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document

class DataIngestionAgent:
    def __init__(self, vector_db_dir="vector_db/"):
        self.vector_db_dir = vector_db_dir
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(persist_directory=vector_db_dir, embedding_function=self.embeddings)

    def _extract_date_from_pdf(self, pdf_path):
        """Extracts appointment date from the PDF."""
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
        """Parses appointment data from PDF."""
        appointments = []
        date = self._extract_date_from_pdf(pdf_path)
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    for _, row in df.iterrows():
                        sl = row.get('SL', None)
                        if not sl or not str(sl).isdigit():
                            continue
                        appointments.append({
                            "content": f"Patient {row['Patient Name']}, Age {row['Age']}, Type {row['Type']}, Category {row['Category']}, SL {row['SL']}",
                            "metadata": {"name": row['Patient Name'], "age": row['Age'], "type": row['Type'], "category": row['Category'], "sl": int(sl)}
                        })
        return appointments

    def ingest_data(self, pdf_path):
        """Ingests data into ChromaDB."""
        appointments = self._extract_appointments_from_pdf(pdf_path)
        documents = [Document(page_content=appt["content"], metadata=appt["metadata"]) for appt in appointments]
        self.vectorstore.add_documents(documents)
        print(f"Successfully stored {len(documents)} appointments into the vector database.")
