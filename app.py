<<<<<<< HEAD
"""
Purpose: Main Streamlit application entry point. 
Handles the UI, file uploads, and chat interface.
"""

import streamlit as st
import os

from config import Config
from utils.constants import APP_TITLE, APP_ICON, PAGE_TITLE, ERROR_NO_PDF, SUCCESS_PROCESS
from utils.helpers import save_uploaded_files, clear_directory
from loaders.pdf_loader import DocumentProcessor
from vectorstore.faiss_db import VectorStoreManager
from chains.qa_chain import QAChatChain

# Set page configuration
st.set_page_config(page_title=PAGE_TITLE, page_icon=APP_ICON, layout="wide")

def init_session_state():
    """Initializes Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = "default_session"
    if "qa_chain_manager" not in st.session_state:
        try:
            st.session_state.qa_chain_manager = QAChatChain()
        except Exception as e:
            st.error(f"Error initializing QA Chain: {e}")
            st.session_state.qa_chain_manager = None

def sidebar_components():
    """Renders the sidebar for document upload and management."""
    with st.sidebar:
        st.title(f"{APP_ICON} {APP_TITLE}")
        st.markdown("Upload PDFs and ask questions about them.")
        
        st.header("1. Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload your PDF files here", 
            type=["pdf"], 
            accept_multiple_files=True
        )
        
        if st.button("Process Documents", type="primary"):
            if not uploaded_files:
                st.warning(ERROR_NO_PDF)
            else:
                with st.spinner("Processing documents... This may take a moment."):
                    # Clear old data to prevent stale vectors if rebuilding
                    clear_directory(Config.DATA_DIR)
                    clear_directory(Config.VECTORDB_DIR)
                    Config.setup_directories()
                    
                    # Save PDFs locally
                    saved_paths = save_uploaded_files(uploaded_files, Config.DATA_DIR)
                    
                    # Process and split
                    processor = DocumentProcessor()
                    chunks = processor.process_documents(saved_paths)
                    
                    # Build Vector DB
                    db_manager = VectorStoreManager()
                    success = db_manager.build_and_save_db(chunks)
                    
                    if success:
                        st.success(SUCCESS_PROCESS)
                    else:
                        st.error("Failed to build the vector database.")
                        
        st.divider()
        st.header("2. Manage Chat")
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            if st.session_state.qa_chain_manager:
                st.session_state.qa_chain_manager.clear_history(st.session_state.session_id)
            st.success("Chat history cleared!")

def main():
    """Main application loop."""
    init_session_state()
    sidebar_components()
    
    st.title("Ask questions from your PDFs 💬")
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display source references if available
            if "sources" in message and message["sources"]:
                with st.expander("View Sources"):
                    for src in message["sources"]:
                        st.caption(f"📄 {src['source']} (Page {src['page']})")
                        st.text(src['snippet'])
    
    # Accept user input
    if prompt := st.chat_input("What would you like to know about the documents?"):
        
        # Check if DB exists before querying
        if not os.path.exists(os.path.join(Config.VECTORDB_DIR, "index.faiss")):
            st.error("Vector database is empty. Please upload and process documents first.")
            return
            
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Generate assistant response
        with st.chat_message("assistant"):
            if not st.session_state.qa_chain_manager:
                st.error("QA Chain not initialized. Check your API Key.")
                return
                
            with st.spinner("Thinking..."):
                try:
                    chain = st.session_state.qa_chain_manager.get_chain()
                    
                    response = chain.invoke(
                        {"input": prompt},
                        config={"configurable": {"session_id": st.session_state.session_id}}
                    )
                    
                    answer = response.get("answer", "I couldn't find an answer.")
                    context_docs = response.get("context", [])
                    
                    st.markdown(answer)
                    
                    # Extract sources safely
                    sources_data = []
                    if context_docs:
                        with st.expander("View Sources"):
                            for i, doc in enumerate(context_docs):
                                source_name = os.path.basename(doc.metadata.get("source", "Unknown"))
                                page_num = doc.metadata.get("page", "Unknown")
                                snippet = doc.page_content[:200] + "..."
                                
                                st.caption(f"📄 {source_name} (Page {page_num})")
                                st.text(snippet)
                                
                                sources_data.append({
                                    "source": source_name,
                                    "page": page_num,
                                    "snippet": snippet
                                })
                                
                    # Save assistant response to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources_data
                    })
                    
                except Exception as e:
                    st.error(f"An error occurred during retrieval: {e}")

if __name__ == "__main__":
    main()
=======
from flask import Flask, request, jsonify, send_from_directory
from prompts import build_email_prompt
from email_generator import generate_email_content
from utils import parse_generated_email
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    
    email_type = data.get('emailType', '')
    recipient = data.get('recipient', '')
    tone = data.get('tone', '')
    length = data.get('length', '')
    additional_details = data.get('additionalDetails', '')
    
    if not additional_details.strip():
        return jsonify({"error": "Please provide some additional details."}), 400
        
    prompt = build_email_prompt(email_type, recipient, tone, length, additional_details)
    raw_response = generate_email_content(prompt)
    
    if raw_response.startswith("Error:") or raw_response.startswith("An error occurred"):
        return jsonify({"error": raw_response}), 500
        
    subject, body = parse_generated_email(raw_response)
    
    return jsonify({
        "subject": subject,
        "body": body
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
>>>>>>> 41774d2c7f5d990ec6a33129693c4f68e2ddf262
