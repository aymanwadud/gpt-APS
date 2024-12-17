import gradio as gr
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from data_ingestion_agent import DataIngestionAgent

# Initialize Vector DB and Agents
VECTOR_DB_DIR = "vector_db/"
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
ingestion_agent = DataIngestionAgent(vector_db_dir=VECTOR_DB_DIR)

# Function to Upload PDF and Ingest Data
def upload_pdf(pdf_file):
    if pdf_file is not None:
        pdf_path = pdf_file.name
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.read())
        ingestion_agent.ingest_data(pdf_path)
        return f"PDF '{pdf_file.name}' successfully ingested into the vector database!"
    return "No PDF uploaded."

# Function to Query Appointments
def query_appointments(user_query):
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=embeddings, retriever=retriever)
    try:
        response = qa_chain.run(user_query)
        return response
    except Exception as e:
        return f"Error: {e}"

# Gradio Interface
with gr.Blocks() as app:
    gr.Markdown("# Appointment Prioritization System (Gradio)")
    
    # Upload PDF Section
    with gr.Row():
        gr.Markdown("### Upload Appointment PDF")
        pdf_input = gr.File(label="Upload PDF")
        upload_button = gr.Button("Ingest PDF")
        upload_output = gr.Textbox(label="Status")
        upload_button.click(upload_pdf, inputs=pdf_input, outputs=upload_output)
    
    # Query Section
    gr.Markdown("### Query Appointments")
    user_query = gr.Textbox(label="Enter your query (e.g., 'List all old patients')")
    query_button = gr.Button("Search")
    query_output = gr.Textbox(label="Results")
    query_button.click(query_appointments, inputs=user_query, outputs=query_output)

# Launch the Gradio App
app.launch()
