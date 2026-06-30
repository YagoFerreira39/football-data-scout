# =========================
# TABLE UI
# =========================

import pandas as pd
import streamlit as st

from src.config.columns import (
    AVAILABLE_LEAGUES_COLUMNS,
    TEAM_TABLE_COLUMNS,
)


def _available_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> list[str]:
    return [col for col in columns if col in df.columns]


def render_available_leagues_table(
    available_leagues_df: pd.DataFrame,
) -> None:
    """
    Render available league-season table.
    """

    st.subheader("Available Leagues")

    cols = _available_columns(
        available_leagues_df,
        AVAILABLE_LEAGUES_COLUMNS,
    )

    st.dataframe(
        available_leagues_df[cols],
        use_container_width=True,
        hide_index=True,
    )


def render_team_stats_table(
    df: pd.DataFrame,
) -> None:
    """
    Render filtered team stats table.
    """

    st.subheader("Teams")

    if df.empty:
        st.info("No teams available for the selected filters.")
        return

    cols = _available_columns(df, TEAM_TABLE_COLUMNS)

    table_df = df[cols].copy()

    if "contestant_name" in table_df.columns:
        table_df = table_df.sort_values("contestant_name")

    column_config = {}

    if "badge_sm" in table_df.columns:
        column_config["badge_sm"] = st.column_config.ImageColumn(
            "Badge",
            width="small",
        )

    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
    )

    