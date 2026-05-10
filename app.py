"""Streamlit dashboard for the Resume Intelligence platform."""

from pathlib import Path

import streamlit as st

from utils.ats import calculate_ats_score, recommend_job_roles
from utils.parser import extract_profile_summary, extract_resume_sections, parse_resume, validate_resume_file
from utils.project_analyzer import analyze_project_quality
from utils.recommendations import build_smart_recommendations, build_strength_indicators
from utils.resume_chat import answer_resume_question
from utils.similarity import build_match_summary
from utils.skills import categorize_skills, extract_skills
from utils.specialization import calculate_role_alignment, detect_specialization
from utils.visualization import (
    create_component_chart,
    create_project_quality_chart,
    create_score_gauge,
    create_skill_category_chart,
    create_specialization_chart,
    create_strength_indicator_chart,
)


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
TARGET_ROLE_OPTIONS = [
    "AI/ML",
    "Data Science",
    "Cloud Engineering",
    "DevOps",
    "Backend Development",
    "Frontend Development",
    "General Software",
]


def save_uploaded_file(uploaded_file) -> Path:
    """Save a Streamlit uploaded file into uploads/ and return its path."""
    UPLOAD_DIR.mkdir(exist_ok=True)
    file_path = UPLOAD_DIR / uploaded_file.name
    file_path.write_bytes(uploaded_file.getbuffer())
    return file_path


def render_sidebar() -> tuple:
    """Render local dashboard inputs."""
    with st.sidebar:
        st.header("Resume Input")
        uploaded_file = st.file_uploader("Upload resume", type=["pdf", "docx"])

        st.header("Career Target")
        target_role = st.selectbox("Select target specialization", TARGET_ROLE_OPTIONS)

        st.header("Job Description")
        job_description = st.text_area(
            "Paste target job description",
            height=220,
            placeholder="Optional: paste a role description for alignment scoring.",
        )

        st.info("Local dashboard mode: uploaded files stay inside the project uploads folder.")

    return uploaded_file, target_role, job_description


def render_overview_tab(
    ats_result: dict,
    specialization_result: dict,
    project_result: dict,
    role_alignment_score: float,
    strength_indicators: dict,
) -> None:
    """Show high-level career positioning metrics."""
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Resume Quality", f"{ats_result['total']}%")
    col2.metric("Specialization", specialization_result["strongest"]["specialization"])
    col3.metric("Project Quality", f"{project_result['score']}%")
    col4.metric("Role Alignment", f"{role_alignment_score}%")

    chart_col1, chart_col2 = st.columns([1, 1])
    with chart_col1:
        st.plotly_chart(create_strength_indicator_chart(strength_indicators), use_container_width=True)
    with chart_col2:
        st.plotly_chart(create_score_gauge(ats_result["total"]), use_container_width=True)
        st.progress(int(role_alignment_score) / 100)


def render_profile_tab(profile_summary: dict, sections: dict, resume_text: str) -> None:
    """Show parsed resume fields without clutter."""
    col1, col2, col3 = st.columns(3)
    col1.metric("Candidate", profile_summary["name"])
    col2.metric("Email", profile_summary["email"])
    col3.metric("Phone", profile_summary["phone"])

    st.subheader("Core Resume Fields")
    with st.expander("Skills", expanded=True):
        st.write(", ".join(profile_summary["skills"]) if profile_summary["skills"] else "Not found")
    with st.expander("Education"):
        st.write(profile_summary["education"])
    with st.expander("Experience"):
        st.write(profile_summary["experience"])

    st.subheader("Detected Sections")
    if sections:
        for section_name, section_text in sections.items():
            with st.expander(section_name.title()):
                st.write(section_text)
    else:
        st.warning("No clear section headings were detected. Use headings like Skills, Experience, Projects, and Education.")

    with st.expander("Full Extracted Text"):
        st.text_area("Resume text", resume_text, height=320, label_visibility="collapsed")


def render_specialization_tab(specialization_result: dict, categorized_skills: dict, skills: list) -> None:
    """Show specialization analysis and technical representation."""
    strongest = specialization_result["strongest"]
    col1, col2 = st.columns(2)
    col1.metric("Detected Specialization", strongest["specialization"])
    col2.metric("Representation Level", specialization_result["representation_level"])

    st.plotly_chart(create_specialization_chart(specialization_result["scores"]), use_container_width=True)
    st.plotly_chart(create_skill_category_chart(skills), use_container_width=True)

    st.subheader("Technical Representation")
    for category, category_skills in categorized_skills.items():
        st.markdown(f"**{category.title()}**")
        st.write(", ".join(category_skills))


def render_projects_tab(project_result: dict) -> None:
    """Show project quality and upgrade ideas."""
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(create_project_quality_chart(project_result), use_container_width=True)
    with col2:
        st.metric("Project Strength", project_result["level"])
        st.write(project_result["summary"])

    if project_result["weak_signals"]:
        st.warning("Basic project signals found: " + ", ".join(project_result["weak_signals"]))

    if project_result["strong_signals"]:
        st.success("Strong project signals found: " + ", ".join(project_result["strong_signals"]))

    st.subheader("Recommended Project Upgrades")
    for project_idea in project_result["recommended_projects"]:
        st.write(f"- {project_idea}")


def render_improvement_tab(
    ats_result: dict,
    smart_recommendations: list,
    match_summary: dict,
) -> None:
    """Show quality-focused improvements and keep keyword details secondary."""
    st.plotly_chart(create_component_chart(ats_result["components"]), use_container_width=True)

    st.subheader("Smart Resume Improvement Suggestions")
    for item in smart_recommendations:
        with st.expander(item["area"], expanded=True):
            st.markdown("**Suggestion**")
            st.write(item["suggestion"])
            st.markdown("**How to improve it**")
            st.write(item["detail"])

    with st.expander("Optional job-description gaps"):
        st.caption("Use these as alignment clues, not as a keyword stuffing checklist.")
        st.markdown("**Missing skills**")
        st.write(", ".join(match_summary["missing_skills"]) if match_summary["missing_skills"] else "No major missing skills found.")
        st.markdown("**Selected missing terms**")
        limited_keywords = match_summary["missing_keywords"][:8]
        st.write(", ".join(limited_keywords) if limited_keywords else "No important missing terms found.")


def render_chat_tab(
    specialization_result: dict,
    project_result: dict,
    smart_recommendations: list,
    role_alignment_score: float,
) -> None:
    """Render a local rule-based resume intelligence chat section."""
    st.subheader("Ask Resume Intelligence Questions")
    example_questions = [
        "Does my resume properly reflect my AI/ML specialization?",
        "Do my projects look strong enough for data science roles?",
        "Which sections weaken my profile?",
        "What should I improve for cloud engineering roles?",
    ]
    selected_question = st.selectbox("Try an example question", [""] + example_questions)
    custom_question = st.text_input("Or ask your own question")
    question = custom_question or selected_question

    if question:
        answer = answer_resume_question(
            question,
            specialization_result,
            project_result,
            smart_recommendations,
            role_alignment_score,
        )
        st.write(answer)
    else:
        st.info("Ask about specialization, project strength, technical depth, weak sections, or career alignment.")


def render_roles_tab(recommended_roles: list, role_alignment_score: float) -> None:
    """Show suitable roles and alignment context."""
    st.metric("Role Alignment Score", f"{role_alignment_score}%")
    st.subheader("Suitable Job Roles")
    cols = st.columns(2)
    for index, role in enumerate(recommended_roles):
        cols[index % 2].success(role)


def main() -> None:
    """Run the Streamlit app."""
    st.set_page_config(page_title="Resume Intelligence Dashboard", page_icon=":bar_chart:", layout="wide")

    st.title("Resume Intelligence & Career Positioning Platform")
    st.caption("Analyze specialization, project quality, technical representation, and role alignment.")

    uploaded_file, target_role, job_description = render_sidebar()

    if not uploaded_file:
        st.info("Upload a PDF or DOCX resume from the sidebar to begin.")
        return

    if not validate_resume_file(uploaded_file.name):
        st.error("Unsupported file type. Please upload a PDF or DOCX resume.")
        return

    try:
        file_path = save_uploaded_file(uploaded_file)
        resume_text = parse_resume(str(file_path))
    except Exception as error:
        st.error(f"Resume parsing failed: {error}")
        return

    if not resume_text:
        st.error("No text could be extracted. Try a text-based PDF or DOCX file.")
        return

    skills = extract_skills(resume_text)
    categorized_skills = categorize_skills(skills)
    sections = extract_resume_sections(resume_text)
    profile_summary = extract_profile_summary(resume_text, skills)
    match_summary = build_match_summary(resume_text, job_description)
    specialization_result = detect_specialization(skills, resume_text, target_role)
    project_result = analyze_project_quality(
        sections,
        specialization_result["strongest"]["specialization"],
        job_description=job_description,
        detected_skills=skills,
    )
    role_alignment_score = calculate_role_alignment(specialization_result, match_summary["similarity_score"])
    ats_result = calculate_ats_score(
        resume_text,
        skills,
        similarity_score=match_summary["similarity_score"],
        missing_keywords_count=match_summary["missing_keywords_count"],
        keyword_density=match_summary["keyword_density"],
    )
    smart_recommendations = build_smart_recommendations(
        specialization_result,
        project_result,
        role_alignment_score,
        sections,
    )
    strength_indicators = build_strength_indicators(
        specialization_result,
        project_result,
        role_alignment_score,
        ats_result["total"],
    )
    recommended_roles = recommend_job_roles(skills)

    st.success(f"Analyzed {uploaded_file.name}")

    overview_tab, specialization_tab, projects_tab, improvement_tab, chat_tab, profile_tab, roles_tab = st.tabs(
        ["Overview", "Specialization", "Projects", "Improvements", "Resume Chat", "Profile", "Role Fit"]
    )

    with overview_tab:
        render_overview_tab(ats_result, specialization_result, project_result, role_alignment_score, strength_indicators)
    with specialization_tab:
        render_specialization_tab(specialization_result, categorized_skills, skills)
    with projects_tab:
        render_projects_tab(project_result)
    with improvement_tab:
        render_improvement_tab(ats_result, smart_recommendations, match_summary)
    with chat_tab:
        render_chat_tab(specialization_result, project_result, smart_recommendations, role_alignment_score)
    with profile_tab:
        render_profile_tab(profile_summary, sections, resume_text)
    with roles_tab:
        render_roles_tab(recommended_roles, role_alignment_score)


if __name__ == "__main__":
    main()
