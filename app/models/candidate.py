from pydantic import BaseModel, Field
from typing import List


class CandidateProfile(BaseModel):
    name: str = ""
    headline: str = ""
    skills: List[str] = Field(default_factory=list)
    programming_languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    experience_years: float = 0
    education: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    target_roles: List[str] = Field(default_factory=list)
