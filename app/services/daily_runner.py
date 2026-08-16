import os
from dotenv import load_dotenv

from app.agents.job_agent import job_agent
from app.models.database import init_db
from app.services.google_sheets import export_jobs_to_sheet
from app.services.gmail_service import send_daily_report

load_dotenv()


def run_daily_agent():
    init_db()

    result = job_agent.invoke({
        "resume_path": os.getenv("RESUME_PATH", "uploads/resume.pdf"),
        "target_role": os.getenv("TARGET_ROLE", "AI Engineer"),
        "target_location": os.getenv("TARGET_LOCATION", "Remote India"),
    })

    jobs = result.get("matched_jobs", [])
    print(f"Found and matched {len(jobs)} jobs.")

    if os.getenv("GOOGLE_SHEET_ID") and os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE"):
        export_jobs_to_sheet()
        print("Google Sheet updated.")

    if os.getenv("DAILY_REPORT_EMAIL") and os.getenv("GMAIL_TOKEN_FILE"):
        send_daily_report()
        print("Gmail report sent.")

    return result


if __name__ == "__main__":
    run_daily_agent()
