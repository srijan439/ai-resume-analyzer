"""
Skill extraction helpers.

The app uses a CSV skill database as the source of truth. This is easy for a
beginner to edit and still follows a scalable pattern: data lives in data/,
matching logic lives in utils/.
"""

import re
from pathlib import Path
from typing import Dict, List

import pandas as pd
import spacy


SKILLS_PATH = Path(__file__).resolve().parent.parent / "data" / "skills.csv"
NLP = spacy.blank("en")
CATEGORY_ALIASES = {
    "frontend": "programming",
    "backend": "programming",
    "api": "programming",
    "data science": "ai/ml",
    "database": "databases",
    "methodology": "soft skills",
}


def load_skills_database() -> pd.DataFrame:
    """Load the skills CSV and normalize text columns."""
    skills_df = pd.read_csv(SKILLS_PATH)
    skills_df["skill"] = skills_df["skill"].str.strip().str.lower()
    skills_df["category"] = skills_df["category"].str.strip().str.lower()
    skills_df["category"] = skills_df["category"].replace(CATEGORY_ALIASES)
    return skills_df.drop_duplicates(subset=["skill"])


def extract_skills(resume_text: str) -> List[str]:
    """
    Match known skills against resume text.

    Regex word boundaries prevent false matches like finding "java" inside
    "javascript". Special characters are escaped so skills such as node.js work.
    """
    skills_df = load_skills_database()
    normalized_resume = resume_text.lower()
    found_skills: List[str] = []

    for skill in skills_df["skill"]:
        pattern = rf"(?<![a-z0-9]){re.escape(skill)}(?![a-z0-9])"
        if re.search(pattern, normalized_resume):
            found_skills.append(skill)

    return sorted(set(found_skills))


def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    """Group matched skills by the category stored in skills.csv."""
    skills_df = load_skills_database()
    category_map = dict(zip(skills_df["skill"], skills_df["category"]))
    categorized: Dict[str, List[str]] = {}

    for skill in skills:
        category = category_map.get(skill, "other")
        categorized.setdefault(category, []).append(skill)

    return categorized


def skill_category_counts(skills: List[str]) -> pd.DataFrame:
    """Return a small dataframe for charts."""
    categorized = categorize_skills(skills)
    rows = [
        {"category": category.title(), "count": len(category_skills)}
        for category, category_skills in categorized.items()
    ]
    return pd.DataFrame(rows).sort_values("count", ascending=False) if rows else pd.DataFrame()


def extract_keywords(text: str, minimum_length: int = 3) -> List[str]:
    """
    Extract simple normalized keywords from text.

    This utility supports missing-keyword analysis without requiring a large NLP
    model download. spaCy can be added later for more advanced noun phrases.
    """
    stop_words = {
        "and",
        "the",
        "for",
        "with",
        "you",
        "your",
        "are",
        "will",
        "from",
        "this",
        "that",
        "have",
        "has",
        "our",
        "job",
        "role",
        "work",
        "team",
    }
    doc = NLP(text.lower())
    words = [
        token.text
        for token in doc
        if not token.is_space and not token.is_punct and re.match(r"[a-zA-Z][a-zA-Z.+#-]+", token.text)
    ]
    keywords = [
        word.strip(".-")
        for word in words
        if len(word.strip(".-")) >= minimum_length and word not in stop_words
    ]
    return sorted(set(keywords))
