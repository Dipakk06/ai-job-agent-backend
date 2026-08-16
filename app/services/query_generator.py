from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class SearchQueries(BaseModel):
    queries: list[str] = Field(min_length=1, max_length=8)


def generate_queries(target_role: str, target_location: str, skills: list[str]) -> list[str]:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    structured = llm.with_structured_output(SearchQueries)

    prompt = ChatPromptTemplate.from_template(
        """Create up to 8 precise job-search queries for a candidate.

Target role: {target_role}
Target location: {target_location}
Skills: {skills}

Include exact and closely related roles. Prefer legitimate job listings and
company career pages. Do not include unrelated roles."""
    )

    result = structured.invoke(
        prompt.format_messages(
            target_role=target_role,
            target_location=target_location,
            skills=", ".join(skills),
        )
    )
    return result.queries
