# YouTube Video Chat with RAG

A production-quality full-stack application that allows users to chat with YouTube videos using Retrieval-Augmented Generation (RAG).

## Architecture

![Architecture](https://via.placeholder.com/800x400.png?text=Architecture+Diagram)

1. **Frontend**: React (Vite) + Tailwind CSS. Provides a modern AI dashboard interface to paste URLs and chat.
2. **Backend**: FastAPI. Exposes `/process-video` and `/chat` REST endpoints.
3. **RAG Pipeline**: 
    - `youtube-transcript-api` to extract transcripts.
    - LangChain `RecursiveCharacterTextSplitter` to chunk the transcript.
    - Google Generative AI Embeddings (`embedding-001`) to vectorize chunks.
    - ChromaDB for local vector storage and semantic search.
    - Gemini (`gemini-2.5-flash`) as the LLM to generate answers strictly based on retrieved chunks.

## Folder Structure

```
youtube-rag/
│
├── backend/
│   ├── main.py              # FastAPI app and endpoints
│   ├── rag.py               # RAG pipeline orchestration
│   ├── transcript.py        # Transcript extraction logic
│   ├── embeddings.py        # Embedding model config
│   ├── vector_store.py      # ChromaDB integration
│   ├── prompts.py           # Strict answering prompt templates
│   ├── config.py            # Environment config (pydantic-settings)
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/                 # React components and API services
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   └── package.json
│
├── chroma_db/               # Auto-generated ChromaDB storage
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API Key

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   Copy `.env.example` to `.env` and add your Google API key:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
5. Start the FastAPI server:
   ```bash
   python main.py
   ```
   The API will run on `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open the application in your browser (usually `http://localhost:5173`).

## Usage

1. Paste a YouTube URL (must be a video with closed captions).
2. Click "Analyze Video". The backend will extract the transcript, chunk it, and store embeddings in ChromaDB.
3. Once processed, you will be taken to the Chat Interface.
4. Ask any question about the video. The AI will answer using only the transcript context and provide the source chunks.

## Future Improvements
- **Audio Transcription**: Integrate Whisper API for videos without closed captions.
- **Timestamp Links**: Enhance transcript extraction to include timestamps and link source chunks directly to the video timeline.
- **Multiple Videos**: Allow users to analyze playlists or multiple videos in one session.
- **User Authentication & Memory**: Save chat history and vector stores per user account.
- **Dockerization**: Add a `Dockerfile` and `docker-compose.yml` for seamless deployment.
