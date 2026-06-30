# =========================
# APP CONTEXT
# =========================

import pandas as pd
import streamlit as st

from src.services.team_stats_service import get_team_stats_data
from src.ui.filters import render_league_filters


@st.cache_data(show_spinner=True)
def load_team_data(
    data_dir: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads and prepares team data once for the app.
    """

    return get_team_stats_data(data_dir=data_dir)


def render_data_source_sidebar() -> str:
    """
    Renders shared sidebar data controls.
    """

    st.sidebar.markdown("### Data")

    data_dir = st.sidebar.text_input(
        "Processed data folder",
        value="data/processed",
    )

    if st.sidebar.button("Reload data"):
        st.cache_data.clear()
        st.rerun()

    return data_dir


def get_team_page_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Shared team page data flow.

    Returns:
    - full team dataframe
    - filtered team dataframe
    - available leagues dataframe
    """

    data_dir = render_data_source_sidebar()

    try:
        team_stats_df, available_leagues_df = load_team_data(data_dir)

    except Exception as exc:
        st.error(f"Could not load data: {exc}")
        st.stop()

    filtered_df = render_league_filters(
        team_stats_df=team_stats_df,
        available_leagues_df=available_leagues_df,
    )

    return team_stats_df, filtered_df, available_leagues_df