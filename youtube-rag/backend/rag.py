import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from transcript import extract_video_id, get_video_transcript, get_transcript_text
from vector_store import add_documents_to_store, similarity_search
from prompts import rag_prompt
from config import settings

def process_video_pipeline(url: str) -> str:
    """
    End-to-end pipeline to extract transcript from a YouTube URL, 
    chunk it, and store it in ChromaDB.
    """
    video_id = extract_video_id(url)
    
    raw_transcript = get_video_transcript(video_id)
    transcript_text = get_transcript_text(raw_transcript)
    
    # Split the transcript into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    
    texts = text_splitter.split_text(transcript_text)
    
    # Create LangChain Documents with metadata
    documents = []
    for i, text in enumerate(texts):
        doc = Document(
            page_content=text,
            metadata={
                "video_id": video_id,
                "chunk_id": str(uuid.uuid4()),
                "chunk_index": i
            }
        )
        documents.append(doc)
        
    # Store embeddings in ChromaDB
    add_documents_to_store(documents)
    
    return video_id

def chat_pipeline(question: str) -> dict:
    """
    Takes a user question, retrieves relevant transcript chunks,
    and generates an answer using Gemini.
    """
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=settings.google_api_key,
        temperature=0.0
    )
    
    # Retrieve relevant chunks
    docs = similarity_search(question, k=4)
    
    # Format the context from retrieved documents
    context_text = "\n\n---\n\n".join([f"Chunk {doc.metadata.get('chunk_index')}:\n{doc.page_content}" for doc in docs])
    
    # Run through the LCEL chain
    chain = rag_prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context_text, "question": question})
    
    # Format the sources for the response
    sources = []
    for doc in docs:
        sources.append({
            "chunk_index": doc.metadata.get("chunk_index"),
            "content": doc.page_content
        })
        
    return {
        "answer": answer,
        "sources": sources
    }
