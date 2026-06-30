# =========================
# SIMILAR TEAMS PAGE
# =========================

import streamlit as st

from src.app_context import get_team_page_data
from src.ui.similar_teams import render_similar_teams_section


st.title("Similar Teams")

team_stats_df, filtered_df, _ = get_team_page_data()

render_similar_teams_section(
    full_team_style_df=team_stats_df,
    filtered_team_style_df=filtered_df,
)