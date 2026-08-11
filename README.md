<<<<<<< HEAD
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
=======
# Agentic AI Showcase

A modern, responsive web application demonstrating Agentic AI features. Built with React (Vite) and Node.js (Express), it features a premium aesthetic with glassmorphism, dark mode, and dynamic components.

## Features

- **Agentic Chat Interface**: An interactive chat UI that shows the agent's intermediate "Thinking" state.
- **Visual Task Planner**: Breaks down complex user requests into step-by-step visual plans, displaying completion status.
- **Execution & Status Simulator**: A dedicated status panel showing real-time updates on what the AI is currently doing (tool usage, background tasks).

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v16+)

### Installation & Setup

1. **Clone or download this repository**
2. **Start the Backend Server**
   ```bash
   cd backend
   npm install
   npm start
   # or node server.js
   ```
   The backend API will run on `http://localhost:3001`

3. **Start the Frontend Application**
   ```bash
   # Open a new terminal
   cd frontend
   npm install
   npm run dev
   ```
   The frontend will typically run on `http://localhost:5173`. Open this URL in your browser.

## Project Structure

- `/frontend` - React application bootstrapped with Vite. Vanilla CSS used for styling.
- `/backend` - Express.js backend containing mock endpoints to simulate AI planning and task execution.

## Future Enhancements
- Connect the backend `/api/chat` route to an actual LLM provider (OpenAI, Gemini).
- Implement Server-Sent Events (SSE) or WebSockets in the backend for true real-time streaming of task progress.
>>>>>>> 4e9b604 (Initial commit or update message)
