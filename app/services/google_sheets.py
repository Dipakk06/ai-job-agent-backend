import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

from app.models.database import Job, SessionLocal

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def export_jobs_to_sheet() -> int:
    credential_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not credential_file or not sheet_id:
        raise RuntimeError("Google Sheets credentials/GOOGLE_SHEET_ID missing.")

    creds = Credentials.from_service_account_file(credential_file, scopes=SCOPES)
    client = gspread.authorize(creds)
    worksheet = client.open_by_key(sheet_id).sheet1

    db = SessionLocal()
    try:
        jobs = db.query(Job).order_by(Job.match_score.desc()).all()
        rows = [[
            "ID", "Company", "Role", "Location", "Match Score",
            "Status", "Matched Skills", "Missing Skills", "URL"
        ]]
        for job in jobs:
            rows.append([
                job.id, job.company, job.title, job.location, job.match_score,
                job.status, job.matched_skills, job.missing_skills, job.url
            ])

        worksheet.clear()
        worksheet.update("A1", rows)
        return len(jobs)
    finally:
        db.close()
