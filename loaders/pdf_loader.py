"""
Purpose: Handles the extraction of text from PDF files and splits the text into chunks.
Integrates with LangChain's Document loaders and Text Splitters.
"""

from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DocumentProcessor:
    """
    Class responsible for loading and processing PDF documents.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the text splitter with given chunk size and overlap.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def process_documents(self, file_paths: List[str]) -> List[Document]:
        """
        Loads multiple PDFs and splits them into smaller document chunks.
        
        Args:
            file_paths (List[str]): List of absolute paths to the PDF files.
            
        Returns:
            List[Document]: A list of LangChain Document objects representing the chunks.
        """
        all_documents = []
        
        for file_path in file_paths:
            try:
                # PyPDFLoader automatically adds 'source' and 'page' to metadata
                loader = PyPDFLoader(file_path)
                documents = loader.load()
                
                # Split documents into chunks
                chunks = self.text_splitter.split_documents(documents)
                all_documents.extend(chunks)
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                
        return all_documents
