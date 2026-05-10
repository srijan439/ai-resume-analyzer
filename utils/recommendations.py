"""Smart resume improvement suggestions."""

from typing import Dict, List


def build_smart_recommendations(
    specialization_result: Dict[str, object],
    project_result: Dict[str, object],
    role_alignment_score: float,
    resume_sections: Dict[str, str],
) -> List[Dict[str, str]]:
    """Create focused mentor-style recommendations instead of generic keyword advice."""
    recommendations: List[Dict[str, str]] = []
    strongest = specialization_result["strongest"]["specialization"]
    representation_level = specialization_result["representation_level"]

    if representation_level != "Strong":
        recommendations.append(
            {
                "area": "Specialization Positioning",
                "suggestion": f"Make the resume clearly read like a {strongest} profile.",
                "detail": "Update the summary, skills, projects, and experience bullets so they repeat the same career direction.",
            }
        )

    if project_result["score"] < 70:
        recommendations.append(
            {
                "area": "Project Strength",
                "suggestion": "Upgrade projects from basic apps to specialization-focused portfolio work.",
                "detail": "Add problem statement, tools used, architecture, dataset or users, deployment, and measurable result.",
            }
        )

    if "summary" not in resume_sections and "profile" not in resume_sections:
        recommendations.append(
            {
                "area": "Professional Summary",
                "suggestion": "Add a short summary that names the target role and strongest technical strengths.",
                "detail": "A good summary should connect your skills, projects, and career goal in 3-4 lines.",
            }
        )

    if role_alignment_score < 55:
        recommendations.append(
            {
                "area": "Career Alignment",
                "suggestion": "Reduce unrelated content and strengthen evidence for the target role.",
                "detail": "Recruiters should understand your direction within the first screen of the resume.",
            }
        )

    if not recommendations:
        recommendations.append(
            {
                "area": "Fine Tuning",
                "suggestion": "Your resume direction is clear. Improve wording and measurable outcomes.",
                "detail": "Focus on stronger action verbs, numbers, and project impact.",
            }
        )

    return recommendations


def build_strength_indicators(
    specialization_result: Dict[str, object],
    project_result: Dict[str, object],
    role_alignment_score: float,
    ats_score: float,
) -> Dict[str, float]:
    """Return high-level resume strength metrics for dashboard cards and charts."""
    return {
        "Specialization": specialization_result["strongest"]["score"],
        "Project Quality": project_result["score"],
        "Role Alignment": role_alignment_score,
        "Resume Quality": ats_score,
    }
