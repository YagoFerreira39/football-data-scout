# =========================
# PLAY STYLE CHART UI
# =========================

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.config.play_style_chart import PLAY_STYLE_COMPARISON_OPTIONS
from src.services.play_style_chart_service import (
    get_play_style_comparison_data,
    get_play_style_team_options,
)


def _format_display_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rounds numeric columns for display.
    """

    view = df.copy()

    numeric_cols = view.select_dtypes(include="number").columns

    for col in numeric_cols:
        view[col] = view[col].round(1)

    return view


def _plot_dot_line_chart(
    comparison_df: pd.DataFrame,
):
    """
    Creates a horizontal dot-line chart.

    It compares a selected team against a benchmark:
    league average or another club.
    """

    chart_df = comparison_df.copy()

    chart_df = chart_df.sort_values(
        "team_score",
        ascending=True,
    ).reset_index(drop=True)

    y_positions = range(len(chart_df))

    team_name = chart_df["team_name"].iloc[0]
    comparison_name = chart_df["comparison_name"].iloc[0]

    fig, ax = plt.subplots(figsize=(9, 6))

    for y_pos, row in zip(y_positions, chart_df.itertuples()):
        ax.plot(
            [row.comparison_score, row.team_score],
            [y_pos, y_pos],
            linewidth=2,
            alpha=0.45,
        )

    ax.scatter(
        chart_df["comparison_score"],
        y_positions,
        s=70,
        label=comparison_name,
        alpha=0.85,
    )

    ax.scatter(
        chart_df["team_score"],
        y_positions,
        s=90,
        label=team_name,
        alpha=0.95,
    )

    ax.set_yticks(list(y_positions))
    ax.set_yticklabels(chart_df["style_area"])

    ax.set_xlim(0, 100)
    ax.set_xlabel("Style score")

    ax.set_title(
        f"{team_name} Play Style Profile",
        fontsize=14,
        fontweight="bold",
        pad=16,
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.25,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, -0.18),
        ncol=2,
        frameon=False,
    )

    plt.tight_layout()

    return fig


def render_play_style_chart_section(
    *,
    full_team_style_df: pd.DataFrame,
    filtered_team_style_df: pd.DataFrame,
) -> None:
    """
    Renders the play-style dot-line comparison chart.
    """

    st.subheader("Play Style Chart")

    if filtered_team_style_df.empty:
        st.info("No teams available for the selected filters.")
        return

    if full_team_style_df.empty:
        st.info("No team style data available.")
        return

    reference_options_df = get_play_style_team_options(
        filtered_team_style_df,
    )

    if reference_options_df.empty:
        st.info("No reference teams available.")
        return

    col1, col2 = st.columns(2)

    with col1:
        selected_team_label = st.selectbox(
            "Club",
            reference_options_df["team_option_label"].tolist(),
            key="play_style_reference_team",
        )

    with col2:
        selected_comparison_label = st.selectbox(
            "Compare against",
            list(PLAY_STYLE_COMPARISON_OPTIONS.keys()),
            key="play_style_comparison_type",
        )

    comparison_type = PLAY_STYLE_COMPARISON_OPTIONS[selected_comparison_label]

    comparison_team_label = None

    if comparison_type == "selected_team":
        comparison_options_df = get_play_style_team_options(
            full_team_style_df,
        )

        comparison_team_label = st.selectbox(
            "Comparison club",
            comparison_options_df["team_option_label"].tolist(),
            key="play_style_comparison_team",
        )

    try:
        comparison_df = get_play_style_comparison_data(
            full_team_style_df,
            team_option_label=selected_team_label,
            comparison_type=comparison_type,
            comparison_team_option_label=comparison_team_label,
        )

    except Exception as exc:
        st.warning(f"Could not build play-style chart: {exc}")
        return

    fig = _plot_dot_line_chart(comparison_df)

    st.pyplot(fig)

    with st.expander("Show chart data"):
        st.dataframe(
            _format_display_df(comparison_df),
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "This chart compares tactical style scores from 0 to 100. It shows play-style profile, not team quality."
    )