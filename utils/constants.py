"""
Purpose: Define constant variables used throughout the application to avoid magic strings.
"""

# UI Constants
APP_TITLE = "AI Research Assistant"
APP_ICON = "📚"
PAGE_TITLE = "AI Research Assistant using LangChain + RAG"

# Error Messages
ERROR_API_KEY = "Please check your GOOGLE_API_KEY in the .env file."
ERROR_NO_PDF = "Please upload at least one PDF document."
ERROR_EMPTY_DB = "Vector database is empty. Please upload documents first."

# Success Messages
SUCCESS_PROCESS = "Documents processed and Vector Database updated successfully!"

# System Prompts
SYSTEM_PROMPT = """You are a helpful and highly knowledgeable AI Research Assistant.
Your task is to answer the user's questions based strictly on the provided context from uploaded documents.
If you do not know the answer based on the context, politely state that the information is not available in the documents.
Do not hallucinate or use outside knowledge.

Context:
{context}
"""
