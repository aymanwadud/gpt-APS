from utils.config import OPENAI_API_KEY
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os
class FeatureExtractionAgent:
    def __init__(self, data_dir="data/"):
        self.data_dir = data_dir
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.vector_db = Chroma(persist_directory=os.path.join(data_dir, "chroma_db"), embedding_function=self.embeddings)

    def extract_features(self, appointment_id):
       docs = self.vector_db.get(ids = [appointment_id])
       if docs and docs.get('metadatas'):
         return {
                "text": docs.get('documents', [''])[0],
                "check_in_time": None,
                "priority_score": 0,
            }
       return None
