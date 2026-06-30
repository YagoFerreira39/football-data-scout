# =========================
# TEAM DETAIL PAGE
# =========================

import streamlit as st

from src.app_context import get_team_page_data
from src.ui.team_detail import render_team_detail_section


st.title("Team Detail")

_, filtered_df, _ = get_team_page_data()

render_team_detail_section(filtered_df)