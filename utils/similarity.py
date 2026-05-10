"""Job description matching utilities."""

from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.skills import extract_keywords, extract_skills


def calculate_similarity(resume_text: str, job_description: str) -> float:
    """Return TF-IDF cosine similarity as a percentage."""
    if not resume_text.strip() or not job_description.strip():
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([resume_text, job_description])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(float(score) * 100, 1)


def find_missing_keywords(resume_text: str, job_description: str, limit: int = 20) -> List[str]:
    """Find important job-description keywords that are absent from the resume."""
    if not job_description.strip():
        return []

    resume_keywords = set(extract_keywords(resume_text))
    job_keywords = extract_keywords(job_description)
    missing = [keyword for keyword in job_keywords if keyword not in resume_keywords]
    return missing[:limit]


def find_missing_skills(resume_text: str, job_description: str) -> List[str]:
    """Compare resume skills with skills mentioned in the job description."""
    resume_skills = set(extract_skills(resume_text))
    job_skills = extract_skills(job_description)
    return sorted(skill for skill in job_skills if skill not in resume_skills)


def calculate_keyword_density(resume_text: str, job_description: str) -> float:
    """
    Calculate how much of the resume is made of target job keywords.

    This is not meant to encourage keyword stuffing. It gives a useful signal
    that the resume language is aligned with the selected job description.
    """
    if not resume_text.strip() or not job_description.strip():
        return 0.0

    resume_words = extract_keywords(resume_text)
    job_keywords = set(extract_keywords(job_description))
    if not resume_words or not job_keywords:
        return 0.0

    matched_keyword_count = sum(1 for word in resume_words if word in job_keywords)
    return round((matched_keyword_count / len(resume_words)) * 100, 1)


def build_match_summary(resume_text: str, job_description: str) -> Dict[str, object]:
    """Bundle all job matching results for the Streamlit page."""
    similarity_score = calculate_similarity(resume_text, job_description)
    missing_keywords = find_missing_keywords(resume_text, job_description)
    missing_skills = find_missing_skills(resume_text, job_description)
    keyword_density = calculate_keyword_density(resume_text, job_description)

    return {
        "similarity_score": similarity_score,
        "missing_keywords": missing_keywords,
        "missing_keywords_count": len(missing_keywords),
        "missing_skills": missing_skills,
        "missing_skills_count": len(missing_skills),
        "keyword_density": keyword_density,
    }
