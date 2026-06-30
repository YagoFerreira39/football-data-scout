# =========================
# SIMILAR TEAMS UI
# =========================

import pandas as pd
import streamlit as st

from src.config.similar_teams import SIMILAR_TEAM_SCOPE_OPTIONS
from src.services.similar_teams_service import (
    get_similar_team_reference_options,
    get_similar_teams,
)


def _format_similar_teams_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats similar teams output for display.
    """

    view = df.copy()

    numeric_cols = view.select_dtypes(include="number").columns

    for col in numeric_cols:
        view[col] = view[col].round(2)

    return view


def render_similar_teams_section(
    *,
    full_team_style_df: pd.DataFrame,
    filtered_team_style_df: pd.DataFrame,
) -> None:
    """
    Renders the Similar Teams section.

    Reference teams are selected from the current filters.
    Candidate teams can come from wider scopes.
    """

    st.subheader("Similar Teams")

    if filtered_team_style_df.empty:
        st.info("No reference teams available for the selected filters.")
        return

    if full_team_style_df.empty:
        st.info("No team style data available.")
        return

    reference_options_df = get_similar_team_reference_options(
        filtered_team_style_df,
    )

    if reference_options_df.empty:
        st.info("No reference teams available.")
        return

    col1, col2, col3 = st.columns([2, 1.5, 1])

    with col1:
        selected_reference_team = st.selectbox(
            "Reference team",
            reference_options_df["team_option_label"].tolist(),
            key="similar_teams_reference_selector",
        )

    with col2:
        selected_scope_label = st.selectbox(
            "Comparison scope",
            list(SIMILAR_TEAM_SCOPE_OPTIONS.keys()),
            index=2,
            key="similar_teams_scope_selector",
        )

    with col3:
        top_n = st.slider(
            "Teams",
            min_value=5,
            max_value=30,
            value=10,
            step=5,
            key="similar_teams_top_n",
        )

    candidate_scope = SIMILAR_TEAM_SCOPE_OPTIONS[selected_scope_label]

    try:
        similar_teams_df = get_similar_teams(
            full_team_style_df,
            reference_team_option_label=selected_reference_team,
            candidate_scope=candidate_scope,
            top_n=top_n,
        )

    except Exception as exc:
        st.warning(f"Could not calculate similar teams: {exc}")
        return

    st.markdown("### Most Similar Teams")

    st.dataframe(
        _format_similar_teams_df(similar_teams_df),
        use_container_width=True,
        hide_index=True,
    )

    chart_cols = [
        "contestant_name",
        "similarity_score",
    ]

    if all(col in similar_teams_df.columns for col in chart_cols):
        chart_df = similar_teams_df[chart_cols].copy()

        st.bar_chart(
            chart_df,
            x="contestant_name",
            y="similarity_score",
        )

    st.caption(
        "Similarity is based on team style scores. It compares profile shape, not team quality."
    )