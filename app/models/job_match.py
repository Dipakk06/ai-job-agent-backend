from pydantic import BaseModel, Field
from typing import List


class JobMatch(BaseModel):
    match_score: int = Field(ge=0, le=100)
    skills_score: int = Field(ge=0, le=100)
    experience_score: int = Field(ge=0, le=100)
    role_score: int = Field(ge=0, le=100)
    location_score: int = Field(ge=0, le=100)
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    recommendation: str
    reason: str
