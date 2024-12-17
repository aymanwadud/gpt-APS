import datetime
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from utils.config import OPENAI_API_KEY
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

class PriorityCalculationAgent:
    def init(self, data_dir="data/"):
        self.data_dir = data_dir
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.vector_db = Chroma(persist_directory=os.path.join(data_dir, "chroma_db"), embedding_function=self.embeddings)
        self.llm = OpenAI(openai_api_key = OPENAI_API_KEY)
    def calculate_priority(self, features, check_in_time = None):
        priority_score = 0.0
        # Rule-based priority: More wait time means higher priority
        if check_in_time:
           wait_time = (datetime.datetime.now() - check_in_time).total_seconds()
           priority_score += wait_time * 0.1
    
        # Weighted factor: Checkup or report have medium priority
        if "report" in features.get("text", "").lower():
           priority_score += 10
    
        if "emergency" in features.get("text", "").lower():
            priority_score += 20
    
        return priority_score
        
    def update_priority_in_db(self, appointment_id, check_in_time = None):
        features = self.get_features_from_db(appointment_id)
        priority_score = self.calculate_priority(features, check_in_time)
        return priority_score
    
    def get_features_from_db(self, appointment_id):
        docs = self.vector_db.get(ids=[appointment_id])
        if docs and docs.get('metadatas'):
           return {
                "text": docs.get('documents', [''])[0],
            }
        return None
        
