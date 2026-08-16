import os
from dotenv import load_dotenv

from app.agents.job_agent import job_agent
from app.models.database import init_db

load_dotenv()


def main():
    init_db()

    result = job_agent.invoke({
        "resume_path": os.getenv("RESUME_PATH", "uploads/resume.pdf"),
        "target_role": os.getenv("TARGET_ROLE", "AI Engineer"),
        "target_location": os.getenv("TARGET_LOCATION", "Remote India"),
    })

    print("\n=== TOP JOB MATCHES ===")
    for i, job in enumerate(result.get("matched_jobs", [])[:10], 1):
        print(
            f"{i}. {job.get('title')} | {job.get('company')} | "
            f"{job.get('match_score')}% | {job.get('url')}"
        )


if __name__ == "__main__":
    main()
