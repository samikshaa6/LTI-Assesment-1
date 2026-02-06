from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from .rag_engine import RAGEngine
from .llm_service import LLMService
from dotenv import load_dotenv

load_dotenv()

# Check for API Key
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    # Fallback if not in env, though it should be.
    # User provided key in prompt: [ENCRYPTION_KEY]
    # STRICTLY FOR DEMO PURPOSES
    API_KEY = "[ENCRYPTION_KEY]"

app = FastAPI(title="Resume Screening AI")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_engine = RAGEngine()
llm_service = LLMService()

# Store formatted text for current session (Simplistic state)
CURRENT_RESUME_TEXT = ""
CURRENT_JD_TEXT = ""

class ChatRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_files(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):
    global CURRENT_RESUME_TEXT, CURRENT_JD_TEXT
    
    # Save temp files
    os.makedirs("temp", exist_ok=True)
    resume_path = f"temp/{resume.filename}"
    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
        
    # Parse Resume
    # Assuming PDF for resume mostly, or txt
    if resume.filename.endswith(".pdf"):
        resume_text = rag_engine.parse_pdf(resume_path)
    else:
        # basic txt handling
         with open(resume_path, "r", encoding="utf-8") as f:
             resume_text = f.read()
             
    # Parse JD (assuming txt usually, but handle file)
    jd_content = await jd.read()
    try:
        jd_text = jd_content.decode("utf-8")
    except:
        # In case it's a PDF
        jd_path = f"temp/{jd.filename}"
        with open(jd_path, "wb") as buffer:
           buffer.write(jd_content)
        jd_text = rag_engine.parse_pdf(jd_path)

    CURRENT_RESUME_TEXT = resume_text
    CURRENT_JD_TEXT = jd_text

    # Analyze
    analysis = llm_service.analyze_match(resume_text, jd_text)
    
    # Index for RAG
    rag_engine.index_document(resume_text, {"source": "resume"})
    
    return {
        "status": "success",
        "analysis": analysis
    }

@app.post("/chat")
async def chat_resume(request: ChatRequest):
    # RAG Retrieval
    relevant_context = rag_engine.retrieve_context(request.question)
    
    # Generate Answer
    answer = llm_service.ask_question(relevant_context, request.question)
    
    return {"answer": answer, "context_used": relevant_context}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
