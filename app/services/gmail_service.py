import base64
import os
from email.mime.text import MIMEText

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from app.models.database import Job, SessionLocal

load_dotenv()

GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def send_daily_report(recipient: str | None = None) -> int:
    recipient = recipient or os.getenv("DAILY_REPORT_EMAIL")
    token_file = os.getenv("GMAIL_TOKEN_FILE")

    if not recipient or not token_file:
        raise RuntimeError("Gmail recipient/token configuration is missing.")

    creds = Credentials.from_authorized_user_file(token_file, GMAIL_SCOPES)
    service = build("gmail", "v1", credentials=creds)

    db = SessionLocal()
    try:
        jobs = (
            db.query(Job)
            .filter(Job.match_score >= 80, Job.status == "NEW")
            .order_by(Job.match_score.desc())
            .limit(10)
            .all()
        )
    finally:
        db.close()

    body = "Good morning!\\n\\nYour AI Job Agent found these high-match opportunities today.\\n\\n"

    if not jobs:
        body += "No new jobs with a match score of 80% or higher were found today.\\n"
    else:
        for i, job in enumerate(jobs, 1):
            body += (
                f"{i}. {job.title}\\n"
                f"Company: {job.company}\\n"
                f"Location: {job.location}\\n"
                f"Match: {job.match_score}%\\n"
                f"Matched: {job.matched_skills}\\n"
                f"Missing: {job.missing_skills}\\n"
                f"Apply: {job.url}\\n"
                "-----------------------------\\n"
            )

    message = MIMEText(body)
    message["to"] = recipient
    message["subject"] = "Your Daily AI Job Report"

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    return len(jobs)
