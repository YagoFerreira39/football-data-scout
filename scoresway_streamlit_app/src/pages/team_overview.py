# =========================
# TEAM OVERVIEW PAGE
# =========================

import streamlit as st

from src.app_context import get_team_page_data
from src.ui.kpis import render_team_stats_kpis
from src.ui.tables import (
    render_available_leagues_table,
    render_team_stats_table,
)


st.title("Team Overview")

team_stats_df, filtered_df, available_leagues_df = get_team_page_data()

render_available_leagues_table(available_leagues_df)

render_team_stats_kpis(filtered_df)

render_team_stats_table(filtered_df)