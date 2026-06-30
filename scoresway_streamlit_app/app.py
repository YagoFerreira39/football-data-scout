# =========================
# STREAMLIT ROUTER
# =========================

import streamlit as st


st.set_page_config(
    page_title="Scoresway Football Data",
    page_icon="⚽",
    layout="wide",
)


# =========================
# PAGES
# =========================

team_overview_page = st.Page(
    "src/pages/team_overview.py",
    title="Overview",
    icon=":material/table_chart:",
    url_path="team-overview",
    default=True,
)

team_detail_page = st.Page(
    "src/pages/team_detail.py",
    title="Team Detail",
    icon=":material/analytics:",
    url_path="team-detail",
)

team_style_page = st.Page(
    "src/pages/team_style.py",
    title="Team Style",
    icon=":material/radar:",
    url_path="team-style",
)

play_style_profile_page = st.Page(
    "src/pages/play_style_profile.py",
    title="Play Style Profile",
    icon=":material/graphic_eq:",
    url_path="play-style-profile",
)

similar_teams_page = st.Page(
    "src/pages/similar_teams.py",
    title="Similar Teams",
    icon=":material/compare_arrows:",
    url_path="similar-teams",
)

opposition_report_page = st.Page(
    "src/pages/opposition_report.py",
    title="Opposition Helper",
    icon=":material/sports_soccer:",
    url_path="opposition-helper",
)

player_overview_page = st.Page(
    "src/pages/player_overview.py",
    title="Overview",
    icon=":material/groups:",
    url_path="player-overview",
)

player_profile_page = st.Page(
    "src/pages/player_profile.py",
    title="Player Profile",
    icon=":material/person_search:",
    url_path="player-profile",
)


# =========================
# NAVIGATION
# =========================

pages = {
    "Team": [
        team_overview_page,
        team_detail_page,
        team_style_page,
        play_style_profile_page,
        similar_teams_page,
        opposition_report_page,
    ],
    "Player": [
        player_overview_page,
        player_profile_page,
    ],
}

selected_page = st.navigation(
    pages,
    position="sidebar",
    expanded=True,
)

selected_page.run()