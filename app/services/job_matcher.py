from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from app.models.job_match import JobMatch
from app.services.scoring import calculate_score


def match_job(candidate_profile: dict, job: dict) -> JobMatch:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    structured = llm.with_structured_output(JobMatch)

    prompt = ChatPromptTemplate.from_template(
        """You are an expert technical recruiter.
Compare the candidate profile with the job listing.

Candidate:
{candidate_profile}

Job title: {job_title}
Company: {company}
Location: {job_location}
Description:
{job_description}

Score skills, experience, role and location from 0-100.
List only skills clearly supported by the candidate as matched.
List important missing skills from the job.
Recommendation must be one of:
HIGH PRIORITY, GOOD MATCH, POSSIBLE MATCH, LOW MATCH.
Do not inflate scores."""
    )

    result = structured.invoke(
        prompt.format_messages(
            candidate_profile=candidate_profile,
            job_title=job.get("title", ""),
            company=job.get("company", ""),
            job_location=job.get("location", ""),
            job_description=job.get("description", ""),
        )
    )

    final_score = calculate_score(
        result.skills_score,
        result.role_score,
        result.experience_score,
        result.location_score,
    )
    return result.model_copy(update={"match_score": final_score})
