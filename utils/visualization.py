"""Plotly chart builders for the dashboard."""

from typing import Dict, List

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils.skills import skill_category_counts


def create_score_gauge(score: float) -> go.Figure:
    """Create an ATS score gauge."""
    figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2f80ed"},
                "steps": [
                    {"range": [0, 50], "color": "#fde2e2"},
                    {"range": [50, 75], "color": "#fff4cc"},
                    {"range": [75, 100], "color": "#dcfce7"},
                ],
            },
        )
    )
    figure.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=10))
    return figure


def create_skill_category_chart(skills: List[str]) -> go.Figure:
    """Create a bar chart of skill counts by category."""
    data = skill_category_counts(skills)
    if data.empty:
        data = pd.DataFrame([{"category": "No skills found", "count": 0}])

    figure = px.bar(
        data,
        x="category",
        y="count",
        color="category",
        text="count",
        title="Skills by Category",
    )
    figure.update_layout(showlegend=False, height=340, margin=dict(l=20, r=20, t=50, b=20))
    return figure


def create_component_chart(component_scores: Dict[str, float]) -> go.Figure:
    """Create a horizontal chart showing ATS component scores."""
    data = pd.DataFrame(
        [{"component": component, "score": score} for component, score in component_scores.items()]
    )
    figure = px.bar(
        data,
        x="score",
        y="component",
        orientation="h",
        text="score",
        title="ATS Score Breakdown",
        color="score",
        color_continuous_scale="Blues",
    )
    figure.update_layout(height=340, margin=dict(l=20, r=20, t=50, b=20))
    return figure


def create_match_chart(match_percentage: float, missing_keywords_count: int) -> go.Figure:
    """Create a compact comparison chart for job-description match quality."""
    data = pd.DataFrame(
        [
            {"metric": "Match %", "value": match_percentage},
            {"metric": "Missing Keywords", "value": missing_keywords_count},
        ]
    )
    figure = px.bar(data, x="metric", y="value", color="metric", text="value")
    figure.update_layout(showlegend=False, height=280, margin=dict(l=20, r=20, t=20, b=20))
    return figure


def create_specialization_chart(specialization_scores: List[Dict[str, object]]) -> go.Figure:
    """Create a chart showing specialization strength across career tracks."""
    data = pd.DataFrame(specialization_scores)
    figure = px.bar(
        data,
        x="specialization",
        y="score",
        color="score",
        text="score",
        title="Specialization Detection",
        color_continuous_scale="Teal",
    )
    figure.update_layout(height=340, margin=dict(l=20, r=20, t=50, b=20), yaxis_range=[0, 100])
    return figure


def create_strength_indicator_chart(strength_indicators: Dict[str, float]) -> go.Figure:
    """Create a radar chart for resume strength indicators."""
    labels = list(strength_indicators.keys())
    values = list(strength_indicators.values())
    figure = go.Figure(
        data=[
            go.Scatterpolar(
                r=values + [values[0]],
                theta=labels + [labels[0]],
                fill="toself",
                name="Resume Strength",
            )
        ]
    )
    figure.update_layout(
        height=360,
        margin=dict(l=30, r=30, t=40, b=20),
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title="Resume Strength Indicators",
    )
    return figure


def create_project_quality_chart(project_result: Dict[str, object]) -> go.Figure:
    """Create a focused project quality gauge."""
    figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=project_result["score"],
            number={"suffix": "%"},
            title={"text": "Project Relevance"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#0f766e"},
                "steps": [
                    {"range": [0, 50], "color": "#fee2e2"},
                    {"range": [50, 75], "color": "#fef3c7"},
                    {"range": [75, 100], "color": "#dcfce7"},
                ],
            },
        )
    )
    figure.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=10))
    return figure
