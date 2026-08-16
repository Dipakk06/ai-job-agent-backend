from app.models.database import Job, SessionLocal

VALID_STATUSES = {
    "NEW", "SAVED", "APPLIED", "INTERVIEW", "REJECTED", "OFFER"
}


def update_job_status(job_id: int, status: str) -> None:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")

    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise ValueError("Job not found")
        job.status = status
        db.commit()
    finally:
        db.close()
