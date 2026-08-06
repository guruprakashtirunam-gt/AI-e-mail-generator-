from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import settings

def get_embeddings_model():
    """Returns the configured Google Generative AI Embeddings model."""
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.google_api_key
    )
