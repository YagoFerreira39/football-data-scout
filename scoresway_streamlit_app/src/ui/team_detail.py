# =========================
# TEAM DETAIL UI
# =========================

import pandas as pd
import streamlit as st

from src.services.team_profile_service import (
    get_selected_team_profile,
    get_team_options,
)
from src.ui.team_header import render_team_header_from_row


def _format_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rounds numeric values for display.
    """

    view = df.copy()

    numeric_cols = view.select_dtypes(include="number").columns

    for col in numeric_cols:
        view[col] = view[col].round(2)

    return view


def render_team_detail_section(
    filtered_df: pd.DataFrame,
) -> None:
    """
    Renders the team detail section below the main team table.
    """

    st.subheader("Team Detail")

    if filtered_df.empty:
        st.info("No team data available for the selected filters.")
        return

    team_options_df = get_team_options(filtered_df)

    if team_options_df.empty:
        st.info("No teams available for the selected filters.")
        return

    selected_team_label = st.selectbox(
        "Select team",
        team_options_df["team_option_label"].tolist(),
    )

    profile = get_selected_team_profile(
        filtered_df,
        team_option_label=selected_team_label,
    )

    overview_df = profile["overview"]

    if not overview_df.empty:
        render_team_header_from_row(overview_df.iloc[0])

    st.markdown("### Overview")

    st.dataframe(
        _format_numeric_columns(profile["overview"]),
        use_container_width=True,
        hide_index=True,
    )

    metric_groups = profile["metric_groups"]

    st.markdown("### Team Metrics")

    tabs = st.tabs(
        [
            "Attacking",
            "Possession",
            "Defending",
            "Duels",
        ]
    )

    tab_keys = [
        "attacking",
        "possession",
        "defending",
        "duels",
    ]

    for tab, group_key in zip(tabs, tab_keys):
        with tab:
            group_df = metric_groups.get(group_key, pd.DataFrame())

            if group_df.empty:
                st.info("No metrics available for this area.")
                continue

            display_df = group_df[
                [
                    "metric",
                    "value",
                    "rank_in_selected_group",
                    "teams_count",
                ]
            ].copy()

            overview_display = profile["overview"].drop(
                columns=["badge_lg", "badge_sm"],
                errors="ignore",
            )

            st.dataframe(
                _format_numeric_columns(overview_display),
                use_container_width=True,
                hide_index=True,
            )