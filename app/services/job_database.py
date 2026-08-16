from app.models.database import Job, SessionLocal


def save_jobs(jobs: list[dict]) -> int:
    db = SessionLocal()
    created = 0

    try:
        for item in jobs:
            url = item.get("url")
            if not url:
                continue

            existing = db.query(Job).filter(Job.url == url).first()

            if existing:
                for field in (
                    "title", "company", "location", "description",
                    "match_score", "skills_score", "experience_score",
                    "role_score", "location_score", "recommendation", "reason"
                ):
                    if field in item:
                        setattr(existing, field, item[field])

                existing.matched_skills = ",".join(item.get("matched_skills", []))
                existing.missing_skills = ",".join(item.get("missing_skills", []))
                continue

            db.add(Job(
                title=item.get("title", ""),
                company=item.get("company", ""),
                location=item.get("location", ""),
                url=url,
                description=item.get("description", ""),
                match_score=item.get("match_score", 0),
                skills_score=item.get("skills_score", 0),
                experience_score=item.get("experience_score", 0),
                role_score=item.get("role_score", 0),
                location_score=item.get("location_score", 0),
                matched_skills=",".join(item.get("matched_skills", [])),
                missing_skills=",".join(item.get("missing_skills", [])),
                recommendation=item.get("recommendation", ""),
                reason=item.get("reason", ""),
                status="NEW",
            ))
            created += 1

        db.commit()
        return created
    finally:
        db.close()
