"""
Purpose: Defines the prompt templates used by the LLM.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from utils.constants import SYSTEM_PROMPT

def get_qa_prompt() -> ChatPromptTemplate:
    """
    Returns the ChatPromptTemplate for the main QA chain.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    return prompt

def get_contextualize_q_prompt() -> ChatPromptTemplate:
    """
    Returns the ChatPromptTemplate for contextualizing the user's question
    based on the chat history.
    """
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    return prompt
