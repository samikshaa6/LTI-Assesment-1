
# AI-Powered Resume Screening Tool

A full-stack application that helps HR professionals screen resumes against job descriptions using AI. It features a RAG (Retrieval-Augmented Generation) system to chat with resumes and provides structured analysis (Match Score, Strengths, Weaknesses).
## Features

- **Smart Analysis**: Matches resumes to job descriptions with a quantified score.
- **RAG Chat**: Ask questions about the candidate
- **Local Privacy**: Embeddings are generated locally on your machine using `sentence-transformers`.
- **High Performance**: Uses Groq's LPU inference for near-instant analysis.

## Prerequisites

- **Python** 
- **Node.js**
- **Groq API Key**

## Installation

### 1. Backend Setup

```bash
cd backend
# Create virtual environment (optional but recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

### 3. Environment Configuration

Create a `.env` file in the `backend/` directory:

```ini
# backend/.env
GROQ_API_KEY=your_groq_api_key_here
```

##Running the Application

### Start the Backend
```bash
# In the backend directory
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*Note: The first run will download the embedding model (all-MiniLM-L6-v2), which may take a few seconds.*

### Start the Frontend
```bash
# In the frontend directory
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

## API Documentation

The backend provides auto-generated Swagger UI documentation.
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints

- `POST /upload`: Uploads `resume` (PDF) and `jd` (Text) for analysis.
- `POST /chat`: Asks a question about the processed resume context.

##Troubleshooting

- **500 Error during Upload**: Usually means the embedding model is still downloading or `sentence-transformers` is missing. Check backend console.
- **400 Error (Model Deprecated)**: Ensure `llm_service.py` is pointing to a supported Groq model (e.g., `llama-3.3-70b-versatile`).


