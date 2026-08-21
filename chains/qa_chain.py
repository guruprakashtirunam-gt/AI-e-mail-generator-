"""
Purpose: Initializes the LLM and builds the retrieval-augmented generation (RAG) chain 
with conversation history.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from config import Config
from vectorstore.faiss_db import VectorStoreManager
from prompts.prompt_template import get_qa_prompt, get_contextualize_q_prompt

class QAChatChain:
    """
    Manages the conversational RAG chain using Google Gemini.
    """
    def __init__(self):
        # Initialize the Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model=Config.LLM_MODEL,
            temperature=0.3, # Low temperature for more factual responses
            google_api_key=Config.GOOGLE_API_KEY
        )
        self.vector_store_manager = VectorStoreManager()
        self.store = {} # In-memory store for session histories
        
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """
        Retrieves or creates a chat message history for a given session ID.
        """
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def clear_history(self, session_id: str):
        """
        Clears the chat history for a given session.
        """
        if session_id in self.store:
            self.store[session_id] = ChatMessageHistory()

    def get_chain(self):
        """
        Builds and returns the history-aware retrieval chain.
        """
        retriever = self.vector_store_manager.get_retriever(k=4)
        
        if not retriever:
            raise ValueError("Vector database not found. Please upload documents first.")

        # 1. Create a history-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            self.llm, retriever, get_contextualize_q_prompt()
        )
        
        # 2. Create the document combining chain (QA)
        qa_chain = create_stuff_documents_chain(self.llm, get_qa_prompt())
        
        # 3. Combine both into a single retrieval chain
        rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)
        
        # 4. Wrap with message history
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
        
        return conversational_rag_chain
