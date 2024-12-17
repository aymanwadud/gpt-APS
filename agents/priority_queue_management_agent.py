from utils.config import OPENAI_API_KEY
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os
import copy
class PriorityQueueManagementAgent:
    def __init__(self, data_dir="data/"):
      self.data_dir = data_dir
      self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
      self.vector_db = Chroma(persist_directory=os.path.join(data_dir, "chroma_db"), embedding_function=self.embeddings)

    def get_prioritized_queue(self):
        """Returns the prioritized queue (appointments sorted by priority)."""
        all_ids = self.vector_db.get()['ids']
        return [copy.copy(appt) for appt in all_ids]
