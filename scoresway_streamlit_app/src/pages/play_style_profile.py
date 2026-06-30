# =========================
# PLAY STYLE PROFILE PAGE
# =========================

import streamlit as st

from src.app_context import get_team_page_data
from src.ui.play_style_profile import render_play_style_profile_section


st.title("Play Style Profile")

team_stats_df, filtered_df, _ = get_team_page_data()

render_play_style_profile_section(
    full_team_style_df=team_stats_df,
    filtered_team_style_df=filtered_df,
)