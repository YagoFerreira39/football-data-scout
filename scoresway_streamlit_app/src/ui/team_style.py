# =========================
# TEAM STYLE UI
# =========================

import pandas as pd
import streamlit as st

from src.services.team_profile_service import get_team_options
from src.services.team_style_service import get_selected_team_style_profile


def _format_style_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats style score tables for display.
    """

    view = df.copy()

    if "score" in view.columns:
        view["score"] = view["score"].round(1)

    return view


def _resolve_selected_team(
    team_options_df: pd.DataFrame,
    selected_team_label: str,
) -> dict:
    """
    Converts a selected team label into team identifiers.
    """

    selected = team_options_df[
        team_options_df["team_option_label"] == selected_team_label
    ]

    if selected.empty:
        raise ValueError("Selected team was not found.")

    row = selected.iloc[0]

    return {
        "team_name": row["contestant_name"],
        "league_name": row["source_league_name"],
        "season": row["source_season"],
    }


def render_team_style_section(
    team_style_df: pd.DataFrame,
) -> None:
    """
    Renders selected team style profile.
    """

    st.subheader("Team Style Profile")

    if team_style_df.empty:
        st.info("No team style data available for the selected filters.")
        return

    team_options_df = get_team_options(team_style_df)

    if team_options_df.empty:
        st.info("No teams available for style profile.")
        return

    selected_team_label = st.selectbox(
        "Select team for style profile",
        team_options_df["team_option_label"].tolist(),
        key="team_style_selector",
    )

    selected_team = _resolve_selected_team(
        team_options_df,
        selected_team_label,
    )

    profile = get_selected_team_style_profile(
        team_style_df,
        team_name=selected_team["team_name"],
        league_name=selected_team["league_name"],
        season=selected_team["season"],
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Strongest Traits")
        st.dataframe(
            _format_style_table(profile["strongest_traits"]),
            use_container_width=True,
            hide_index=True,
        )

    with col2:
        st.markdown("### Weakest Traits")
        st.dataframe(
            _format_style_table(profile["weakest_traits"]),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("### Style Scores")

    st.dataframe(
        _format_style_table(profile["style_scores"]),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Style Chart")

    chart_df = profile["style_scores"].copy()

    chart_df = chart_df[
        chart_df["style_area"] != "Overall Style Intensity"
    ]

    st.bar_chart(
        chart_df,
        x="style_area",
        y="score",
    )