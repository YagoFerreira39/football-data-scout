# =========================
# TEAM STYLE PAGE
# =========================

import streamlit as st

from src.app_context import get_team_page_data
from src.ui.team_style import render_team_style_section


st.title("Team Style Profile")

_, filtered_df, _ = get_team_page_data()

render_team_style_section(filtered_df)