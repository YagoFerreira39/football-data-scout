import streamlit as st

from config.theme import apply_theme


st.set_page_config(
    page_title="RoleRadar - Football Data Analysis & Scouting",
    page_icon="⚽",
    layout="wide",
)

apply_theme()


home_page = st.Page(
    "pages/home.py",
    title="Home",
    icon="⚽",
    url_path="home",
)

leagues_page = st.Page(
    "pages/leagues.py",
    title="Leagues",
    icon="🌍",
    url_path="leagues",
)

teams_page = st.Page(
    "pages/teams.py",
    title="Teams",
    icon="👥",
    url_path="teams",
)

players_page = st.Page(
    "pages/players.py",
    title="Players",
    icon="👤",
    url_path="players",
)

pg = st.navigation(
    [
        home_page,
        leagues_page,
        teams_page,
        players_page,
    ],
    position="hidden",
)

with st.sidebar:
    st.page_link(
        home_page,
        label="Home",
        icon="⚽",
    )

pg.run()