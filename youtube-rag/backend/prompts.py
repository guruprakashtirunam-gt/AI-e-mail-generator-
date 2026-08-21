from langchain_core.prompts import PromptTemplate

RAG_PROMPT_TEMPLATE = """You are a helpful assistant.

Answer ONLY using the provided transcript context.

If the answer is not available in the transcript, respond:
'I couldn't find that information in the video transcript.'

Never make up information.
Always cite the transcript chunks used.

Context:
{context}

Question: {question}

Answer:"""

rag_prompt = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
