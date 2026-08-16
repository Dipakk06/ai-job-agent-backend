from langgraph.graph import END, START, StateGraph

from app.models.state import JobAgentState
from app.services.job_cleaner import deduplicate_jobs
from app.services.job_database import save_jobs
from app.services.job_matcher import match_job
from app.services.query_generator import generate_queries
from app.services.resume_analyzer import analyze_resume
from app.services.resume_parser import extract_resume_text
from app.tools.firecrawl_tool import search_jobs as firecrawl_search


def load_profile(state: JobAgentState):
    text = extract_resume_text(state["resume_path"])
    return {"resume_text": text}


def analyze_candidate(state: JobAgentState):
    profile = analyze_resume(state["resume_text"])
    return {"candidate_profile": profile.model_dump()}


def search_jobs(state: JobAgentState):
    profile = state["candidate_profile"]
    queries = generate_queries(
        state.get("target_role", ""),
        state.get("target_location", ""),
        profile.get("skills", []),
    )

    all_jobs = []
    for query in queries:
        try:
            all_jobs.extend(firecrawl_search(query, limit=10))
        except Exception as exc:
            print(f"Search failed for {query!r}: {exc}")

    return {"search_queries": queries, "jobs": all_jobs}


def clean_jobs(state: JobAgentState):
    return {"jobs": deduplicate_jobs(state.get("jobs", []))}


def match_jobs(state: JobAgentState):
    matched = []
    for i, job in enumerate(state.get("jobs", []), 1):
        try:
            match = match_job(state["candidate_profile"], job)
            matched.append({
                **job,
                **match.model_dump(),
            })
            print(f"Matched {i}/{len(state.get('jobs', []))}: {job.get('title', '')}")
        except Exception as exc:
            print(f"Match failed for {job.get('url', '')}: {exc}")

    matched.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    return {"matched_jobs": matched}


def save_database(state: JobAgentState):
    count = save_jobs(state.get("matched_jobs", []))
    print(f"Saved {count} new jobs.")
    return {}


def build_graph():
    graph = StateGraph(JobAgentState)

    graph.add_node("load_profile", load_profile)
    graph.add_node("analyze_candidate", analyze_candidate)
    graph.add_node("search_jobs", search_jobs)
    graph.add_node("clean_jobs", clean_jobs)
    graph.add_node("match_jobs", match_jobs)
    graph.add_node("save_database", save_database)

    graph.add_edge(START, "load_profile")
    graph.add_edge("load_profile", "analyze_candidate")
    graph.add_edge("analyze_candidate", "search_jobs")
    graph.add_edge("search_jobs", "clean_jobs")
    graph.add_edge("clean_jobs", "match_jobs")
    graph.add_edge("match_jobs", "save_database")
    graph.add_edge("save_database", END)

    return graph.compile()


job_agent = build_graph()
