# =========================
# KPI UI
# =========================

import pandas as pd
import streamlit as st


def _format_number(value: float | None, decimals: int = 2) -> str:
    if value is None or pd.isna(value):
        return "-"

    return f"{value:.{decimals}f}"


def _safe_mean(df: pd.DataFrame, column: str) -> float | None:
    if column not in df.columns or df.empty:
        return None

    return df[column].mean()


def render_team_stats_kpis(df: pd.DataFrame) -> None:
    """
    Render basic team stats KPI row.
    """

    st.subheader("Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    teams_count = (
        df["contestant_name"].nunique()
        if "contestant_name" in df.columns
        else len(df)
    )

    avg_possession = _safe_mean(df, "Possession Percentage")
    avg_goals = _safe_mean(df, "goals_per_game")
    avg_shots = _safe_mean(df, "shots_per_game")
    avg_ppda = _safe_mean(df, "PPDA")

    col1.metric("Teams", teams_count)

    col2.metric(
        "Avg Possession",
        f"{avg_possession:.1f}%" if avg_possession is not None else "-",
    )

    col3.metric(
        "Avg Goals/Game",
        _format_number(avg_goals, decimals=2),
    )

    col4.metric(
        "Avg Shots/Game",
        _format_number(avg_shots, decimals=2),
    )

    col5.metric(
        "Avg PPDA",
        _format_number(avg_ppda, decimals=2),
    )