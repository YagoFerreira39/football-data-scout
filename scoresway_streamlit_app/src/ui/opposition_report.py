# =========================
# OPPOSITION REPORT UI
# =========================

import pandas as pd
import streamlit as st

from src.services.opposition_report_service import (
    get_opposition_team_options,
    get_selected_opposition_report,
)


def _format_display_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rounds numeric columns for display.
    """

    view = df.copy()

    numeric_cols = view.select_dtypes(include="number").columns

    for col in numeric_cols:
        view[col] = view[col].round(2)

    return view


def _render_dataframe(
    title: str,
    df: pd.DataFrame,
) -> None:
    """
    Renders a dataframe with a fallback message.
    """

    st.markdown(f"### {title}")

    if df.empty:
        st.info("No data available.")
        return

    st.dataframe(
        _format_display_df(df),
        use_container_width=True,
        hide_index=True,
    )


def render_opposition_report_section(
    *,
    full_team_style_df: pd.DataFrame,
    filtered_team_style_df: pd.DataFrame,
) -> None:
    """
    Renders the Opposition Report Helper section.

    Opponent selector uses current filters.
    Report calculations use the full team style dataframe.
    """

    st.subheader("Opposition Report Helper")

    if filtered_team_style_df.empty:
        st.info("No opponents available for the selected filters.")
        return

    if full_team_style_df.empty:
        st.info("No team style data available.")
        return

    opponent_options_df = get_opposition_team_options(
        filtered_team_style_df,
    )

    if opponent_options_df.empty:
        st.info("No opponent options available.")
        return

    selected_opponent_label = st.selectbox(
        "Select opponent",
        opponent_options_df["team_option_label"].tolist(),
        key="opposition_report_team_selector",
    )

    try:
        report = get_selected_opposition_report(
            full_team_style_df,
            team_option_label=selected_opponent_label,
        )

    except Exception as exc:
        st.warning(f"Could not build opposition report: {exc}")
        return

    # =========================
    # Overview
    # =========================

    _render_dataframe(
        "Opponent Overview",
        report["overview"],
    )

    # =========================
    # Main points
    # =========================

    col1, col2 = st.columns(2)

    with col1:
        _render_dataframe(
            "Main Strengths",
            report["main_strengths"],
        )

    with col2:
        _render_dataframe(
            "Possible Vulnerabilities",
            report["possible_vulnerabilities"],
        )

    _render_dataframe(
        "Preparation Focus",
        report["preparation_focus"],
    )

    # =========================
    # Profiles
    # =========================

    tabs = st.tabs(
        [
            "Attack",
            "Defence",
            "Style Scores",
            "Supporting Metrics",
        ]
    )

    with tabs[0]:
        _render_dataframe(
            "How They Attack",
            report["attacking_profile"][
                [
                    "style_area",
                    "score",
                    "band",
                    "interpretation",
                ]
            ],
        )

    with tabs[1]:
        _render_dataframe(
            "How They Defend",
            report["defensive_profile"][
                [
                    "style_area",
                    "score",
                    "band",
                    "interpretation",
                ]
            ],
        )

    with tabs[2]:
        _render_dataframe(
            "Style Scores",
            report["style_scores"],
        )

        chart_df = report["style_scores"].copy()

        if not chart_df.empty and {"style_area", "score"}.issubset(chart_df.columns):
            chart_df = chart_df[
                chart_df["style_area"] != "Overall Style Intensity"
            ]

            st.bar_chart(
                chart_df,
                x="style_area",
                y="score",
            )

    with tabs[3]:
        key_metrics = report["key_metrics"].copy()

        if key_metrics.empty:
            st.info("No supporting metrics available.")
        else:
            display_cols = [
                "metric_group",
                "metric",
                "value",
                "rank_in_selected_group",
                "teams_count",
            ]

            available_cols = [
                col for col in display_cols
                if col in key_metrics.columns
            ]

            _render_dataframe(
                "Supporting Metrics",
                key_metrics[available_cols],
            )

    st.caption(
        "This is a data-led preparation helper. Use video and match context before turning it into a final opposition report."
    )