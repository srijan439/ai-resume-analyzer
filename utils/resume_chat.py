"""Rule-based resume intelligence Q&A."""

from typing import Dict, List


def answer_resume_question(
    question: str,
    specialization_result: Dict[str, object],
    project_result: Dict[str, object],
    smart_recommendations: List[Dict[str, str]],
    role_alignment_score: float,
) -> str:
    """
    Answer common career-oriented resume questions.

    This is intentionally rule-based for local development. Later, this module
    can be replaced with an LLM while the Streamlit UI stays the same.
    """
    question_lower = question.lower().strip()
    strongest = specialization_result["strongest"]["specialization"]
    representation = specialization_result["representation_level"].lower()

    if not question_lower:
        return "Ask a question about specialization, project strength, technical depth, or role alignment."

    if any(term in question_lower for term in ["specialization", "reflect", "expertise", "properly"]):
        return (
            f"Your resume currently shows a {representation} {strongest} signal. "
            "Strengthen it by making the summary, skills, projects, and experience point toward the same role."
        )

    if any(term in question_lower for term in ["project", "projects", "portfolio"]):
        return (
            f"Project quality is rated as {project_result['level']} ({project_result['score']}%). "
            f"{project_result['summary']} Recommended project directions: "
            f"{', '.join(project_result['recommended_projects'][:4])}."
        )

    if any(term in question_lower for term in ["weaken", "weak", "improve", "better"]):
        top_recommendations = smart_recommendations[:3]
        return "Focus on: " + " ".join(
            f"{item['area']}: {item['suggestion']}" for item in top_recommendations
        )

    if any(term in question_lower for term in ["cloud", "devops", "data science", "ai", "ml", "backend", "frontend"]):
        return (
            f"For that direction, your current role alignment score is {role_alignment_score}%. "
            "Add role-specific projects, technical tools, measurable outcomes, and clearer domain wording."
        )

    return (
        "I would improve the resume by clarifying the target role, strengthening project evidence, "
        "adding measurable outcomes, and making technical wording more specific."
    )
