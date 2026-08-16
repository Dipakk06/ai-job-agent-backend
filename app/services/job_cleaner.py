from urllib.parse import urlsplit, urlunsplit


def canonical_url(url: str) -> str:
    parts = urlsplit(url.strip())
    return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path.rstrip("/"), "", ""))


def deduplicate_jobs(jobs: list[dict]) -> list[dict]:
    seen = set()
    unique = []

    for job in jobs:
        url = job.get("url", "")
        if not url:
            continue

        normalized = canonical_url(url)
        if normalized in seen:
            continue

        seen.add(normalized)
        job = dict(job)
        job["url"] = normalized
        unique.append(job)

    return unique
