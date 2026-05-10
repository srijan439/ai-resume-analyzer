"""Project quality analysis for resume intelligence."""

from typing import Dict, List


BASIC_PROJECT_SIGNALS = {"calculator", "todo", "to-do", "landing page", "portfolio", "crud", "static website"}
STRONG_PROJECT_SIGNALS = {
    "AI/ML": ["nlp system", "computer vision", "ml pipeline", "recommendation system", "model deployment"],
    "Data Science": ["analytics dashboard", "forecasting model", "etl pipeline", "business intelligence report"],
    "Cloud Engineering": ["serverless app", "cloud deployment", "scalable architecture", "storage pipeline"],
    "DevOps": ["ci/cd pipeline", "kubernetes deployment", "monitoring dashboard", "dockerized application"],
    "Backend Development": ["rest api", "authentication system", "microservice", "database-backed application"],
    "Frontend Development": ["responsive dashboard", "component library", "interactive web app", "accessibility-focused ui"],
}


def analyze_project_quality(
    resume_sections: Dict[str, str],
    specialization: str,
    job_description: str = "",
    detected_skills: List[str] = None,
) -> Dict[str, object]:
    """Evaluate whether projects support the detected or target specialization."""
    project_text = resume_sections.get("projects", "")
    project_lower = project_text.lower()
    
    # Base recommendations from specialization
    recommendations = list(STRONG_PROJECT_SIGNALS.get(specialization, []))
    
    # Add "General Software" fallback if specialization is unknown
    if not recommendations:
        recommendations = ["Full-stack web application", "API integration project", "System design case study"]

    if not project_text:
        return {
            "score": 20,
            "level": "Needs projects",
            "summary": "No clear Projects section was detected.",
            "weak_signals": ["Missing dedicated project evidence"],
            "strong_signals": [],
            "recommended_projects": recommendations,
        }

    weak_signals = sorted(signal for signal in BASIC_PROJECT_SIGNALS if signal in project_lower)
    strong_signals = sorted(
        signal for signal in STRONG_PROJECT_SIGNALS.get(specialization, []) if signal in project_lower
    )
    technical_depth_score = _score_technical_depth(project_lower)
    score = min(100, 35 + technical_depth_score + len(strong_signals) * 12 - len(weak_signals) * 8)

    # Dynamic updates based on job description
    if job_description:
        from utils.skills import extract_keywords
        jd_keywords = extract_keywords(job_description)
        # Suggest projects that use missing high-value JD keywords
        dynamic_suggestions = [f"Build a project using {k}" for k in jd_keywords[:3] if k not in project_lower]
        recommendations = dynamic_suggestions + recommendations

    return {
        "score": max(0, score),
        "level": _project_level(score),
        "summary": _build_project_summary(score, weak_signals, strong_signals),
        "weak_signals": weak_signals,
        "strong_signals": strong_signals,
        "recommended_projects": recommendations[:6],
    }


def _score_technical_depth(project_text: str) -> int:
    """Reward projects that mention real implementation depth."""
    depth_terms = {
        "api",
        "database",
        "pipeline",
        "model",
        "deployment",
        "authentication",
        "dashboard",
        "docker",
        "cloud",
        "testing",
    }
    return min(40, sum(4 for term in depth_terms if term in project_text))


def _project_level(score: int) -> str:
    """Return a readable quality label."""
    if score >= 75:
        return "Strong"
    if score >= 50:
        return "Moderate"
    return "Needs upgrade"


def _build_project_summary(score: int, weak_signals: List[str], strong_signals: List[str]) -> str:
    """Explain the project-quality result in mentor-style language."""
    if score >= 75:
        return "Projects show practical depth and support the selected specialization."
    if weak_signals and not strong_signals:
        return "Projects look too basic for the specialization. Add deeper, domain-specific implementations."
    return "Projects have some useful signals, but they need clearer technical depth and stronger outcomes."
