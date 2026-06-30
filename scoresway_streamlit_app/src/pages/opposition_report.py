# =========================
# OPPOSITION REPORT PAGE
# =========================

import streamlit as st

from src.app_context import get_team_page_data
from src.ui.opposition_report import render_opposition_report_section


st.title("Opposition Report Helper")

team_stats_df, filtered_df, _ = get_team_page_data()

render_opposition_report_section(
    full_team_style_df=team_stats_df,
    filtered_team_style_df=filtered_df,
)