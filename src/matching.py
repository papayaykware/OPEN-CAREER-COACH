def compute_match(cv: dict, job: dict) -> dict:
    skills = set(cv["skills"])
    reqs = set(job["requirements"])

    overlap = skills.intersection(reqs)
    score = round(len(overlap) / max(len(reqs), 1), 2)

    return {
        "score": score,
        "matched_skills": list(overlap),
        "missing_skills": list(reqs - skills)
    }
