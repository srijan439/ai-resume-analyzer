"""Specialization and career-alignment analysis."""

from typing import Dict, List


SPECIALIZATION_RULES = {
    "AI/ML": {
        "skills": {"python", "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "nlp"},
        "keywords": {"model", "dataset", "training", "prediction", "classification", "nlp", "computer vision"},
    },
    "Data Science": {
        "skills": {"python", "sql", "pandas", "numpy", "scikit-learn"},
        "keywords": {"analytics", "visualization", "dashboard", "statistics", "insights", "forecasting"},
    },
    "Cloud Engineering": {
        "skills": {"aws", "azure", "gcp", "ec2", "s3", "lambda"},
        "keywords": {"cloud", "serverless", "deployment", "infrastructure", "scalable"},
    },
    "DevOps": {
        "skills": {"docker", "kubernetes", "jenkins", "git", "github", "gitlab", "ci/cd"},
        "keywords": {"pipeline", "automation", "container", "monitoring", "deployment"},
    },
    "Backend Development": {
        "skills": {"python", "java", "node.js", "django", "flask", "fastapi", "sql", "mongodb"},
        "keywords": {"api", "backend", "microservices", "database", "authentication"},
    },
    "Frontend Development": {
        "skills": {"javascript", "typescript", "html", "css", "react", "angular", "vue"},
        "keywords": {"ui", "frontend", "responsive", "component", "interface"},
    },
}


def detect_specialization(skills: List[str], resume_text: str, target_role: str = "") -> Dict[str, object]:
    """Score how strongly the resume represents each specialization."""
    skill_set = set(skills)
    text_lower = resume_text.lower()
    target_lower = target_role.lower()
    results = []

    for name, rule in SPECIALIZATION_RULES.items():
        matched_skills = sorted(skill_set.intersection(rule["skills"]))
        matched_keywords = sorted(keyword for keyword in rule["keywords"] if keyword in text_lower)
        target_bonus = 10 if name.lower() in target_lower else 0
        score = min(100, len(matched_skills) * 12 + len(matched_keywords) * 7 + target_bonus)

        results.append(
            {
                "specialization": name,
                "score": score,
                "matched_skills": matched_skills,
                "matched_keywords": matched_keywords,
            }
        )

    results.sort(key=lambda item: item["score"], reverse=True)
    naturally_strongest = results[0] if results else {"specialization": "General Software", "score": 0}

    # If a target role is selected, prioritize it as the 'strongest' for UI analysis
    target_result = next(
        (r for r in results if r["specialization"].lower() == target_role.lower()), None
    )
    strongest = target_result if target_result else naturally_strongest

    return {
        "strongest": strongest,
        "scores": results,
        "target_role": target_role or "Not provided",
        "representation_level": _representation_label(strongest["score"]),
    }


def calculate_role_alignment(specialization_result: Dict[str, object], job_match_score: float) -> float:
    """Combine specialization strength and job match into a career alignment score."""
    specialization_score = specialization_result["strongest"]["score"]
    return round((specialization_score * 0.65) + (job_match_score * 0.35), 1)


def _representation_label(score: float) -> str:
    """Convert a numeric specialization score into a readable label."""
    if score >= 75:
        return "Strong"
    if score >= 45:
        return "Developing"
    return "Weak"
