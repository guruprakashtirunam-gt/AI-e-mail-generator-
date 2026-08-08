<<<<<<< HEAD
# AI Research Assistant using LangChain + RAG 📚

A production-quality web application that allows users to upload PDF documents and ask questions about their content. The assistant uses Retrieval-Augmented Generation (RAG) to ensure it answers *only* using information retrieved from the uploaded documents, complete with source citations.

---

## 🌟 Features
- **Multi-PDF Upload**: Upload and process multiple PDF documents simultaneously.
- **Accurate RAG Architecture**: Answers questions strictly based on uploaded context to prevent AI hallucinations.
- **Source Transparency**: Displays the exact document name, page number, and text snippet used to generate the answer.
- **Conversational Memory**: Remembers previous questions and context within a chat session.
- **Local Vector Database**: Uses FAISS and HuggingFace embeddings running locally to ensure privacy and avoid embedding API costs.
- **Modern UI**: Clean, responsive interface built with Streamlit.

## 💻 Technology Stack
- **Language**: Python 3.12+
- **Framework**: Streamlit
- **Orchestration**: LangChain (LCEL)
- **LLM**: Google Gemini (via `langchain-google-genai`)
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Document Processing**: PyPDFLoader

## 📁 Folder Structure
```text
AI-Research-Assistant/
├── app.py                      # Main Streamlit application entry point
├── config.py                   # Centralized configuration and path management
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables file
├── chains/
│   └── qa_chain.py             # LangChain RAG and conversational memory setup
├── embeddings/
│   └── embedding_model.py      # HuggingFace local embeddings initialization
├── loaders/
│   └── pdf_loader.py           # PyPDF extraction and chunking logic
├── prompts/
│   └── prompt_template.py      # System prompts and LCEL chat templates
├── utils/
│   ├── constants.py            # Global UI strings and prompt definitions
│   └── helpers.py              # File saving and directory management utilities
└── vectorstore/
    └── faiss_db.py             # FAISS index creation, saving, and loading
```

## 🚀 Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/AI-Research-Assistant.git
   cd AI-Research-Assistant
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Environment Variables

Copy the example environment file and add your Google Gemini API key:
```bash
cp .env.example .env
```
Open `.env` and configure your API key:
```env
GOOGLE_API_KEY=your_actual_google_api_key_here
```

## ▶️ How to Run

Start the Streamlit server:
```bash
streamlit run app.py
```
The application will open in your default browser at `http://localhost:8501`.

## 💡 Example Usage
1. Open the application in your browser.
2. In the sidebar, upload one or more PDF files (e.g., a research paper or a manual).
3. Click **"Process Documents"** and wait for the vector database to build.
4. In the main chat window, ask a question like: *"What is the main conclusion of the study on page 3?"*
5. The AI will answer, and you can click **"View Sources"** to verify the exact page it read.

## 📸 Screenshots
*(Add screenshots of your application here once deployed)*
- **Upload & Process UI**
- **Chat Interface with Source Citations**

## 🔮 Future Enhancements
- Support for additional file formats (Word, TXT, CSV, Web URLs).
- Integration with other LLMs (OpenAI, Anthropic, or local models via Ollama).
- User authentication and persistent cloud storage for vector databases.
- Hybrid search (Keyword + Vector similarity).

## 📄 License
This project is licensed under the [MIT License](LICENSE).

## 👤 Author
**Your Name**  
*Senior AI Engineer*  
[LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)

---
**Topics/Tags:** `python` `langchain` `streamlit` `rag` `generative-ai` `faiss` `huggingface` `pdf-parsing` `gemini-api`
=======
# AI Email Generator

An AI-powered email generator built with Streamlit and Google Gemini.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your Gemini API Key.
   ```bash
   cp .env.example .env
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```
>>>>>>> 41774d2c7f5d990ec6a33129693c4f68e2ddf262
