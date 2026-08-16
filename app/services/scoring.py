def calculate_score(
    skills_score: int,
    role_score: int,
    experience_score: int,
    location_score: int,
) -> int:
    return round(
        skills_score * 0.40
        + role_score * 0.25
        + experience_score * 0.20
        + location_score * 0.15
    )
