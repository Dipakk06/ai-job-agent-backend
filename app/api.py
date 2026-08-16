from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.chatbot import chat_with_jobs
from app.models.database import Job, SessionLocal


app = FastAPI(
    title="AI Job Agent API",
    version="1.0.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# CANDIDATE PROFILE
# --------------------------------------------------

CANDIDATE_PROFILE = """
The candidate is an AI Engineer.

Main skills:

Python
Machine Learning
Deep Learning
Generative AI
LLMs
RAG
LangChain
LangGraph
FastAPI
AI Agents

The candidate is looking for AI Engineer,
Generative AI Engineer, Machine Learning Engineer
and related roles, preferably remote or in India.
"""


# --------------------------------------------------
# MODELS
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


# --------------------------------------------------
# DATABASE HELPER
# --------------------------------------------------

def job_to_dict(job: Job):
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "url": job.url,
        "description": job.description,
        "match_score": job.match_score,
        "skills_score": job.skills_score,
        "experience_score": job.experience_score,
        "role_score": job.role_score,
        "location_score": job.location_score,
        "matched_skills": (
            job.matched_skills.split(",")
            if job.matched_skills
            else []
        ),
        "missing_skills": (
            job.missing_skills.split(",")
            if job.missing_skills
            else []
        ),
        "recommendation": job.recommendation,
        "reason": job.reason,
        "status": job.status,
    }


# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.get("/api/health")
def health():

    db = SessionLocal()

    try:
        count = db.query(Job).count()

        return {
            "status": "ok",
            "jobs_loaded": count,
        }

    finally:
        db.close()


# --------------------------------------------------
# GET ALL JOBS
# --------------------------------------------------

@app.get("/api/jobs")
def get_jobs():

    db = SessionLocal()

    try:
        jobs = (
            db.query(Job)
            .order_by(Job.match_score.desc())
            .all()
        )

        return [job_to_dict(job) for job in jobs]

    finally:
        db.close()


# --------------------------------------------------
# GET SINGLE JOB
# --------------------------------------------------

@app.get("/api/jobs/{job_id}")
def get_job(job_id: int):

    db = SessionLocal()

    try:
        job = (
            db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found",
            )

        return job_to_dict(job)

    finally:
        db.close()


# --------------------------------------------------
# CHATBOT
# --------------------------------------------------

@app.post(
    "/api/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty",
        )

    db = SessionLocal()

    try:

        jobs = (
            db.query(Job)
            .order_by(Job.match_score.desc())
            .all()
        )

        job_data = [
            job_to_dict(job)
            for job in jobs
        ]

    finally:
        db.close()

    if not job_data:
        return {
            "response": (
                "No jobs are currently loaded. "
                "Please run the job search first."
            )
        }

    try:

        answer = chat_with_jobs(
            message=request.message,
            jobs=job_data,
            candidate_profile=CANDIDATE_PROFILE,
        )

        return {
            "response": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Chatbot error: {str(e)}",
        )