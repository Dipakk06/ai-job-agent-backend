import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

load_dotenv()


def _client():
    key = os.getenv("FIRECRAWL_API_KEY")

    if not key:
        raise RuntimeError(
            "FIRECRAWL_API_KEY is missing."
        )

    return FirecrawlApp(api_key=key)


def search_jobs(
    query: str,
    limit: int = 10,
) -> list[dict]:
    """
    Search jobs using Firecrawl.

    Supports current Firecrawl SDK responses such as:

        response.web

    and older/dict-style responses such as:

        response.data
        response["web"]
        response["data"]
    """

    response = _client().search(
        query,
        limit=limit,
    )

    # --------------------------------------------------
    # 1. Current Firecrawl SDK response
    # --------------------------------------------------

    data = getattr(response, "web", None)

    # --------------------------------------------------
    # 2. Older object-style response
    # --------------------------------------------------

    if data is None:
        data = getattr(response, "data", None)

    # --------------------------------------------------
    # 3. Dictionary response
    # --------------------------------------------------

    if data is None and isinstance(response, dict):
        data = (
            response.get("web")
            or response.get("data")
            or []
        )

    data = data or []

    print(
        f"Firecrawl found {len(data)} results "
        f"for: {query}"
    )

    jobs = []

    for item in data:

        # ----------------------------------------------
        # Convert Pydantic/object result to dict
        # ----------------------------------------------

        if hasattr(item, "model_dump"):
            item = item.model_dump()

        elif hasattr(item, "_dict_"):
            item = vars(item)

        elif not isinstance(item, dict):
            continue

        item = item or {}

        metadata = item.get(
            "metadata"
        ) or {}

        # ----------------------------------------------
        # Extract fields
        # ----------------------------------------------

        title = (
            item.get("title")
            or metadata.get("title")
            or ""
        )

        url = (
            item.get("url")
            or metadata.get("url")
            or ""
        )

        description = (
            item.get("description")
            or item.get("snippet")
            or metadata.get("description")
            or ""
        )

        company = (
            item.get("company")
            or metadata.get("company")
            or ""
        )

        location = (
            item.get("location")
            or metadata.get("location")
            or ""
        )

        # ----------------------------------------------
        # Only keep actual URLs
        # ----------------------------------------------

        if not url:
            continue

        jobs.append(
            {
                "title": str(title).strip(),
                "url": str(url).strip(),
                "description": str(
                    description
                ).strip(),
                "company": str(
                    company
                ).strip(),
                "location": str(
                    location
                ).strip(),
                "source": "Firecrawl",
                "search_query": query,
            }
        )

    print(
        f"Normalized {len(jobs)} jobs "
        f"for: {query}"
    )

    return jobs