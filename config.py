"""
Purpose: Centralizes environment loading and global configuration settings.
Integrates with the rest of the project by providing configuration variables safely.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class to store environment variables and global settings.
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Path settings
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    VECTORDB_DIR = os.path.join(DATA_DIR, "faiss_index")
    
    # Model settings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    LLM_MODEL = "gemini-1.5-flash"
    
    @classmethod
    def setup_directories(cls):
        """Ensure necessary directories exist."""
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.VECTORDB_DIR, exist_ok=True)

# Initialize directories on import
Config.setup_directories()
