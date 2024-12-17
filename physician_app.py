import streamlit as st
from agents.data_ingestion_agent import DataIngestionAgent

def main():
    st.title("Physician Appointment Management")
    st.header("Upload Appointment Schedule PDF")

    # Initialize agent
    ingestion_agent = DataIngestionAgent()

    uploaded_file = st.file_uploader("Upload your PDF here", type=["pdf"])

    if uploaded_file is not None:
        try:
            with open("temp.pdf", "wb") as f:
              f.write(uploaded_file.read())
            ingestion_agent.ingest_data('temp.pdf')
            st.success("Appointments loaded successfully!")
        except Exception as e:
           st.error(f"Error loading appointments: {e}")


if __name__ == "__main__":
    main()