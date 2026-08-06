import os
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from embeddings import get_embeddings_model

# Get absolute path for chroma_db at the project root
CHROMA_DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))

def get_vector_store() -> Chroma:
    """Returns the Chroma vector store instance."""
    embeddings = get_embeddings_model()
    return Chroma(
        collection_name="youtube_transcripts",
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_DIR
    )

def add_documents_to_store(documents: list[Document]):
    """Adds documents to the Chroma vector store."""
    vector_store = get_vector_store()
    vector_store.add_documents(documents)

def similarity_search(query: str, k: int = 4) -> list[Document]:
    """Performs a similarity search on the vector store."""
    vector_store = get_vector_store()
    return vector_store.similarity_search(query, k=k)
