import datetime
from utils.config import OPENAI_API_KEY
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

class RealTimeMonitoringAgent:
    def init(self, data_dir="data/"):
        self.data_dir = data_dir
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.vector_db = Chroma(persist_directory=os.path.join(data_dir, "chroma_db"), embedding_function=self.embeddings)
        self.checked_in = {}
        
    def check_in(self, appointment_id):
        self.checked_in[appointment_id] = datetime.datetime.now()
        return self.checked_in[appointment_id]
    
    def get_check_in_time(self, appointment_id):
        return self.checked_in.get(appointment_id, None)
