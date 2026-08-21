# Simple Local RAG Pipeline

This is a lightweight, fully local Retrieval-Augmented Generation (RAG) pipeline built using Python. 

It demonstrates how to ingest a text document, store its embeddings in a local vector database, retrieve relevant context based on a user query, and generate an answer using a local Large Language Model (LLM)—all without needing an internet connection for external APIs like OpenAI!

## Tech Stack
* **Framework:** [LangChain](https://www.langchain.com/)
* **Vector Database:** [ChromaDB](https://www.trychroma.com/)
* **Embeddings Model:** `all-MiniLM-L6-v2` (via HuggingFace)
* **Local LLM:** `gpt2` (via HuggingFace Transformers)

## Prerequisites

**Important:** You must use **Python 3.12** or **Python 3.11**. 
*(Do not use Python 3.13+ as many Machine Learning libraries like PyTorch and ChromaDB do not yet have pre-compiled wheels for it, which will cause installation errors).*

## Installation

1. Open a terminal in this project folder.
2. (Optional but recommended) Create and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```powershell
   pip install langchain langchain-community sentence-transformers chromadb transformers torch langchain-text-splitters
   ```
   *(Note: Downloading PyTorch might take a few minutes depending on your internet speed).*

## Usage

Run the pipeline by executing the script:
```powershell
python rag_pipeline.py
```

The first time you run the script, it will download the AI models (`all-MiniLM-L6-v2` and `gpt2`) to your local machine. Subsequent runs will be much faster.

## How it Works

The script (`rag_pipeline.py`) follows these 8 steps:
1. **Load Document:** Takes a sample document (a Wikipedia article about Mango).
2. **Chunking:** Splits the text into small, manageable chunks of 350 characters.
3. **Embeddings:** Converts each chunk into a mathematical vector using `sentence-transformers`.
4. **Vector Store:** Saves those vectors into a local Chroma vector database.
5. **User Query:** Accepts a query (e.g., *"What vitamins are in mango?"*).
6. **Retrieval:** Searches the Chroma database for the most relevant chunk of text.
7. **Prompt Construction:** Combines the retrieved chunk with the user's query into a strict prompt.
8. **Generation:** Passes the prompt to a local LLM (`gpt2`) to generate the final answer!
