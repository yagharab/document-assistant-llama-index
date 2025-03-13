import streamlit as st
import os
from document_processor import DocumentProcessor

st.set_page_config(
    page_title="Smart Document Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'processor' not in st.session_state:
    st.session_state.processor = DocumentProcessor()
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

def main():
    st.title("📚 Smart Document Assistant")
    st.write("Upload your PDF documents and ask questions about them!")

    # File upload
    uploaded_files = st.file_uploader(
        "Upload your PDF documents",
        type=['pdf'],
        accept_multiple_files=True
    )

    if uploaded_files:
        # Track new files
        new_files = [f for f in uploaded_files if f.name not in st.session_state.uploaded_files]
        
        if new_files:
            # Save new files
            for file in new_files:
                with open(os.path.join("data", file.name), "wb") as f:
                    f.write(file.getbuffer())
                st.session_state.uploaded_files.append(file.name)
            
            # Load documents
            with st.spinner("Processing new documents..."):
                st.session_state.processor.load_documents()
            st.success(f"Processed {len(new_files)} new document(s)!")

        # Display loaded documents
        st.write("### Currently Loaded Documents")
        for idx, filename in enumerate(st.session_state.uploaded_files, 1):
            st.write(f"{idx}. {filename}")

        # Document summary
        if st.button("Generate Summary of All Documents"):
            with st.spinner("Generating summary..."):
                summary = st.session_state.processor.get_document_summary()
                st.write("### Document Summary")
                st.write(summary)

        # Query interface
        st.write("### Ask Questions")
        st.write("You can ask questions about any of the loaded documents!")
        query = st.text_input("What would you like to know about the documents?")
        
        if query:
            with st.spinner("Finding answer..."):
                response = st.session_state.processor.query_documents(query)
                st.write("### Answer")
                st.write(response)

if __name__ == "__main__":
    main()