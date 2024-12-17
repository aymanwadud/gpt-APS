import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from data_ingestion_agent import DataIngestionAgent

# Initialize ChromaDB and LangChain
VECTOR_DB_DIR = "vector_db/"
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)

# Initialize agents
ingestion_agent = DataIngestionAgent(vector_db_dir=VECTOR_DB_DIR)

def main():
    st.title("Smart Appointment Prioritization System")

    # File Upload for PDF
    uploaded_file = st.file_uploader("Upload Appointment PDF", type=["pdf"])
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        ingestion_agent.ingest_data("temp.pdf")
        st.success("Appointments successfully ingested into the vector database!")

    # Query Appointments using Natural Language
    user_query = st.text_input("Ask about appointments (e.g., 'Show all old patients').")
    if user_query:
        retriever = vectorstore.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=embeddings, retriever=retriever)
        response = qa_chain.run(user_query)
        st.write("**Response:**")
        st.write(response)

if __name__ == "__main__":
    main()
