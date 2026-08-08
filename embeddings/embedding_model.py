"""
Purpose: Initializes and provides the HuggingFace embedding model.
Used to convert document chunks and user queries into vector representations.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from config import Config

def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Instantiates and returns the HuggingFace embeddings model specified in config.
    
    Returns:
        HuggingFaceEmbeddings: The initialized embedding model.
    """
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},  # Change to 'cuda' if GPU is available
            encode_kwargs={'normalize_embeddings': True}
        )
        return embeddings
    except Exception as e:
        raise RuntimeError(f"Failed to load embedding model: {e}")
