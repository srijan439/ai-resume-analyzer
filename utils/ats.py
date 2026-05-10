"""
ATS scoring engine.

The score is intentionally transparent. Real ATS tools differ, so this project
uses explainable scoring factors that a learner can inspect and improve.
"""

import re
from typing import Dict, List


IMPORTANT_SECTIONS = ["experience", "education", "skills", "projects", "summary"]
ACTION_KEYWORDS = ["built", "developed", "implemented", "led", "designed", "improved", "managed"]


def calculate_ats_score(
    resume_text: str,
    skills: List[str],
    similarity_score: float = 0,
    missing_keywords_count: int = 0,
    keyword_density: float = 0,
) -> Dict[str, object]:
    """
    Calculate ATS score and return both total and component scores.

    Args:
        resume_text: Extracted resume text.
        skills: Skills found in the resume.
        similarity_score: Cosine similarity percentage against job description.
        missing_keywords_count: Missing keyword count from job description.
        keyword_density: Resume keyword-density percentage from target job terms.
    """
    text_lower = resume_text.lower()

    section_score = _score_sections(text_lower)
    skill_score = min(25, len(skills) * 3)
    keyword_density_score = _score_keyword_density(text_lower, keyword_density)
    completeness_score = _score_completeness(resume_text)
    formatting_score = _score_formatting(resume_text)
    similarity_component = round(min(15, similarity_score * 0.15), 1)

    penalty = min(8, missing_keywords_count * 0.5)
    total_score = section_score + skill_score + keyword_density_score
    total_score += completeness_score + formatting_score + similarity_component
    total_score = max(0, min(100, total_score - penalty))

    return {
        "total": round(total_score, 1),
        "components": {
            "Resume sections": section_score,
            "Skills matched": skill_score,
            "Keyword density": keyword_density_score,
            "Completeness": completeness_score,
            "Formatting": formatting_score,
            "Job match": similarity_component,
        },
    }


def _score_sections(text_lower: str) -> int:
    """Award points when important resume sections are present."""
    matched_sections = sum(1 for section in IMPORTANT_SECTIONS if section in text_lower)
    return min(20, matched_sections * 4)


def _score_keyword_density(text_lower: str, keyword_density: float) -> int:
    """Reward job keyword alignment and action verbs used in achievements."""
    matched_keywords = sum(1 for keyword in ACTION_KEYWORDS if keyword in text_lower)
    action_verb_score = min(6, matched_keywords * 2)
    density_score = min(9, keyword_density * 0.3)
    return round(action_verb_score + density_score, 1)


def _score_completeness(resume_text: str) -> int:
    """Score whether the resume has enough substance to analyze."""
    word_count = len(resume_text.split())
    if word_count >= 500:
        return 15
    if word_count >= 300:
        return 12
    if word_count >= 150:
        return 8
    return 4


def _score_formatting(resume_text: str) -> int:
    """Approximate ATS-friendly formatting with text-based signals."""
    score = 0
    if "\n" in resume_text and len(resume_text.splitlines()) >= 8:
        score += 5
    if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", resume_text):
        score += 5
    if re.search(r"\d", resume_text):
        score += 5
    return score


def get_recommendations(
    resume_text: str,
    skills: List[str],
    ats_score: float,
    missing_keywords: List[str],
) -> List[str]:
    """Generate practical recommendations based on analysis results."""
    text_lower = resume_text.lower()
    recommendations: List[str] = []

    if len(skills) < 8:
        recommendations.append("Add a dedicated skills section with more role-relevant tools and technologies.")
    if "experience" not in text_lower and "work experience" not in text_lower:
        recommendations.append("Add an Experience section with job titles, company names, dates, and impact.")
    if "education" not in text_lower:
        recommendations.append("Add an Education section so ATS systems can identify your background quickly.")
    if not any(keyword in text_lower for keyword in ACTION_KEYWORDS):
        recommendations.append("Use action verbs such as developed, implemented, improved, led, and designed.")
    if not re.search(r"\d", resume_text):
        recommendations.append("Include measurable outcomes such as percentages, revenue, users, time saved, or team size.")
    if missing_keywords:
        recommendations.append("Add the most relevant missing job-description keywords naturally where they are truthful.")
    if ats_score < 70:
        recommendations.append("Tailor the resume summary and skills section for this specific job description.")

    return recommendations or ["Your resume covers the major ATS basics. Keep tailoring keywords for each job."]


def build_resume_update_plan(
    resume_text: str,
    resume_sections: Dict[str, str],
    match_summary: Dict[str, object],
) -> List[Dict[str, str]]:
    """
    Suggest which resume sections to update for the target job description.

    The goal is to guide the user toward truthful, section-specific edits rather
    than dumping every missing keyword into one place.
    """
    update_plan: List[Dict[str, str]] = []
    missing_skills = match_summary.get("missing_skills", [])
    missing_keywords = match_summary.get("missing_keywords", [])
    similarity_score = match_summary.get("similarity_score", 0)
    keyword_density = match_summary.get("keyword_density", 0)
    text_lower = resume_text.lower()

    if not missing_skills and not missing_keywords and not similarity_score:
        return [
            {
                "section": "Job Description",
                "priority": "Required",
                "update": "Paste a target job description in the sidebar.",
                "reason": "The app needs a job description before it can tell which resume sections to update.",
            }
        ]

    if similarity_score < 60:
        update_plan.append(
            {
                "section": "Professional Summary",
                "priority": "High",
                "update": "Rewrite the summary to mention the target role, strongest matching skills, and domain keywords.",
                "reason": "A low job match score usually means the resume introduction is not aligned with the job description.",
            }
        )

    if missing_skills:
        skill_text = ", ".join(missing_skills[:8])
        update_plan.append(
            {
                "section": "Skills",
                "priority": "High",
                "update": f"Add relevant missing skills only if you genuinely have them: {skill_text}.",
                "reason": "ATS systems often scan the skills section first for role-specific tools and technologies.",
            }
        )

    if missing_keywords:
        keyword_text = ", ".join(missing_keywords[:10])
        update_plan.append(
            {
                "section": "Experience",
                "priority": "High",
                "update": f"Use these missing keywords naturally inside achievement bullets: {keyword_text}.",
                "reason": "Keywords are strongest when they appear inside real work experience with measurable impact.",
            }
        )

    project_keywords = {"project", "built", "developed", "implemented", "api", "model", "dashboard", "system"}
    if project_keywords.intersection(set(missing_keywords)) or "projects" not in resume_sections:
        update_plan.append(
            {
                "section": "Projects",
                "priority": "Medium",
                "update": "Add or improve projects that prove the tools and responsibilities mentioned in the job description.",
                "reason": "Projects help beginners show practical proof when professional experience is limited.",
            }
        )

    education_keywords = {"degree", "bachelor", "master", "computer", "science", "certification", "certified"}
    if education_keywords.intersection(set(missing_keywords)) or "education" not in text_lower:
        update_plan.append(
            {
                "section": "Education / Certifications",
                "priority": "Medium",
                "update": "Add relevant degree, coursework, certifications, or training that matches the job requirements.",
                "reason": "Some ATS systems filter for education and certification requirements.",
            }
        )

    if keyword_density < 20 and missing_keywords:
        update_plan.append(
            {
                "section": "Overall Wording",
                "priority": "Medium",
                "update": "Use the employer's wording where it is accurate, especially for tools, responsibilities, and role title.",
                "reason": "Low keyword density means the resume language is not close enough to the job-description language.",
            }
        )

    if not re.search(r"\d", resume_text):
        update_plan.append(
            {
                "section": "Experience / Projects",
                "priority": "Medium",
                "update": "Add numbers to achievements, such as percentages, users, time saved, accuracy, revenue, or team size.",
                "reason": "Metrics make resume bullets stronger for both recruiters and ATS-style scoring.",
            }
        )

    return update_plan or [
        {
            "section": "Resume Tailoring",
            "priority": "Low",
            "update": "Your resume already maps well to this job description. Make small wording changes for the exact role.",
            "reason": "No major missing skills or keywords were detected.",
        }
    ]


def recommend_job_roles(skills: List[str]) -> List[str]:
    """Recommend suitable roles from matched skills."""
    skill_set = set(skills)
    role_rules = {
        "Python Developer": {"python", "django", "flask", "fastapi", "sql"},
        "Frontend Developer": {"javascript", "html", "css", "react", "angular", "vue"},
        "Data Analyst": {"sql", "pandas", "numpy", "excel", "tableau", "power bi"},
        "Machine Learning Engineer": {"python", "machine learning", "deep learning", "tensorflow", "pytorch"},
        "DevOps Engineer": {"docker", "kubernetes", "jenkins", "git", "aws"},
        "Cloud Engineer": {"aws", "azure", "gcp", "docker", "kubernetes"},
        "Backend Developer": {"node.js", "django", "flask", "fastapi", "sql", "mongodb"},
    }

    scored_roles = []
    for role, required_skills in role_rules.items():
        matched = len(skill_set.intersection(required_skills))
        if matched:
            scored_roles.append((role, matched))

    scored_roles.sort(key=lambda item: item[1], reverse=True)
    return [role for role, _ in scored_roles[:4]] or ["Software Developer", "Junior Developer"]
