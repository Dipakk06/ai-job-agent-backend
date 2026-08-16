from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from app.models.candidate import CandidateProfile


def analyze_resume(resume_text: str) -> CandidateProfile:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    structured = llm.with_structured_output(CandidateProfile)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert technical recruiter.
Extract only information supported by the resume. Never invent details.
Identify technical skills, programming languages, frameworks, tools,
experience, education, projects, certifications, and plausible target roles."""
        ),
        ("human", "Resume:\n\n{resume_text}"),
    ])

    return structured.invoke(
        prompt.format_messages(resume_text=resume_text)
    )
