"""
Purpose: Manages the FAISS vector database. Handles creating, saving, 
loading, and querying the vector store.
"""

import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from embeddings.embedding_model import get_embedding_model
from config import Config

class VectorStoreManager:
    """
    Class responsible for managing the FAISS vector database.
    """
    def __init__(self):
        self.embeddings = get_embedding_model()
        self.db_path = Config.VECTORDB_DIR

    def build_and_save_db(self, documents: List[Document]) -> bool:
        """
        Builds the FAISS database from document chunks and saves it locally.
        
        Args:
            documents (List[Document]): The document chunks to index.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if not documents:
                print("No documents provided to build the vector database.")
                return False
                
            # Create FAISS index from documents
            vector_store = FAISS.from_documents(documents, self.embeddings)
            
            # Save the index locally
            vector_store.save_local(self.db_path)
            return True
            
        except Exception as e:
            print(f"Error building vector database: {e}")
            return False

    def load_db(self) -> FAISS:
        """
        Loads the FAISS database from the local directory.
        
        Returns:
            FAISS: The loaded FAISS vector store instance.
        """
        try:
            if not os.path.exists(os.path.join(self.db_path, "index.faiss")):
                raise FileNotFoundError("FAISS index not found. Please process documents first.")
                
            # Allow dangerous deserialization is required for FAISS local loading in newer LangChain versions
            vector_store = FAISS.load_local(
                self.db_path, 
                self.embeddings,
                allow_dangerous_deserialization=True 
            )
            return vector_store
            
        except Exception as e:
            print(f"Error loading vector database: {e}")
            return None

    def get_retriever(self, k: int = 4):
        """
        Returns a retriever interface for the vector store.
        
        Args:
            k (int): Number of most relevant chunks to return.
            
        Returns:
            Retriever: A LangChain retriever.
        """
        vector_store = self.load_db()
        if vector_store:
            # Search type 'similarity' is default, can also use 'mmr'
            return vector_store.as_retriever(search_kwargs={"k": k})
        return None
