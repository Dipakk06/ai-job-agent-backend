from typing import Any, Dict, List, TypedDict


class JobAgentState(TypedDict, total=False):
    resume_path: str
    resume_text: str
    candidate_profile: Dict[str, Any]
    target_role: str
    target_location: str
    search_queries: List[str]
    jobs: List[Dict[str, Any]]
    matched_jobs: List[Dict[str, Any]]
    daily_report: str
