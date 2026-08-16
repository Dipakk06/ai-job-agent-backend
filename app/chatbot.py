import os
import json
from typing import List, Dict

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_job_context(jobs: List[Dict]) -> str:
    context = []

    for i, job in enumerate(jobs[:20], start=1):
        context.append({
            "rank": i,
            "title": job.get("title", ""),
            "company": job.get("company", ""),
            "location": job.get("location", ""),
            "url": job.get("url", ""),
            "description": job.get("description", "")[:2000],
            "match_score": job.get(
                "match_score",
                job.get("score", 0)
            ),
            "matched_skills": job.get(
                "matched_skills",
                []
            ),
            "missing_skills": job.get(
                "missing_skills",
                []
            ),
        })

    return json.dumps(
        context,
        indent=2
    )


def chat_with_jobs(
    message: str,
    jobs: List[Dict],
    candidate_profile: str = "",
) -> str:

    job_context = build_job_context(jobs)

    system_prompt = f"""
You are an AI Job Search Assistant.

You help the candidate understand, compare,
summarize and prioritize job opportunities.

Candidate profile:
{candidate_profile}

Available jobs:
{job_context}

Rules:

1. Use only the provided job data.
2. Never invent job information.
3. Never invent salary information.
4. Never invent company information.
5. Never invent skills or requirements.
6. If information is unavailable, say:
   "Not available in the job data."
7. Mention match scores when relevant.
8. Explain why a job is recommended.
9. Compare jobs when requested.
10. Keep responses concise and useful.
11. Use Markdown.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )

    return response.choices[0].message.content