from pathlib import Path
import re

import numpy as np
import pandas as pd
import streamlit as st

from config.theme import apply_theme
from src import league_map
from src.wyscout_data_loader import WyscoutDataLoader
from components.components import Components


st.set_page_config(
    page_title="Team | RoleRadar",
    page_icon="⚽",
    layout="wide",
)

apply_theme()


# =========================
# Constants
# =========================

components = Components()

player_col = "player"
team_col = "team_within_selected_timeframe"
position_col = "position"
age_col = "age"
minutes_col = "minutes_played"
nationality_col = "birth_country"

country_col = "league_country"
league_col = "league_name"
season_col = "season"

# =========================
# Load data
# =========================

data_loader = WyscoutDataLoader()

@st.cache_data
def load_data() -> pd.DataFrame:
    df = data_loader.prepare_wyscout_data()
    df.columns = df.columns.str.strip()

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    return df

df = load_data()

# =========================
# Helpers
# =========================

def slugify(value: str) -> str:
    value = str(value).lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")

def get_dataframe_height(row_count: int) -> int:
    if row_count >= 18:
        return 738

    if row_count >= 16:
        return 600

    if row_count >= 10:
        return 400

    return 280


# =========================
# Read selected context
# =========================

query_params = st.query_params

country_slug = query_params.get("country")
league_slug = query_params.get("league")
season_slug = query_params.get("season")
team_slug = query_params.get("team")

selected_country = st.session_state.get("selected_country")
selected_league = st.session_state.get("selected_league")
selected_season = st.session_state.get("selected_season")
selected_team = st.session_state.get("selected_team")


# =========================
# Resolve context from URL if needed
# =========================

if selected_country and selected_league and selected_season and selected_team:
    team_df = df[
        (df[country_col] == selected_country)
        & (df[league_col] == selected_league)
        & (df[season_col] == selected_season)
        & (df[team_col] == selected_team)
    ].copy()

elif country_slug and league_slug and season_slug and team_slug:
    df["country_slug"] = df[country_col].apply(slugify)
    df["league_slug"] = df[league_col].apply(slugify)
    df["season_slug"] = df[season_col].apply(slugify)
    df["team_slug"] = df[team_col].apply(slugify)

    team_df = df[
        (df["country_slug"] == country_slug)
        & (df["league_slug"] == league_slug)
        & (df["season_slug"] == season_slug)
        & (df["team_slug"] == team_slug)
    ].copy()

    if team_df.empty:
        st.error("No data found for the selected team.")
        st.stop()

    selected_country = team_df[country_col].iloc[0]
    selected_league = team_df[league_col].iloc[0]
    selected_season = team_df[season_col].iloc[0]
    selected_team = team_df[team_col].iloc[0]

    st.session_state["selected_country"] = selected_country
    st.session_state["selected_league"] = selected_league
    st.session_state["selected_season"] = selected_season
    st.session_state["selected_team"] = selected_team

else:
    st.warning("No team selected. Go back to the league page and select a team.")
    st.stop()


if team_df.empty:
    st.error("No data found for the selected team.")
    st.stop()


# =========================
# Header
# =========================

st.markdown(
    f"""
    <div class="team-header">
        <div class="team-header-kicker">Team Profile</div>
        <div class="team-header-title">{selected_team}</div>
        <div class="team-header-meta">
            <span class="team-header-pill">{selected_league}</span>
            <span class="team-header-pill">{selected_country}</span>
            <span class="team-header-pill">{selected_season}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================
# KPI boxes
# =========================

total_players = team_df[player_col].nunique()

total_nationalities = team_df[nationality_col].nunique()

average_age = team_df[age_col].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Players</div>
            <div class="kpi-value">{total_players}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Nationalities</div>
            <div class="kpi-value">{total_nationalities}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Age</div>
            <div class="kpi-value">{average_age:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.divider()


# =========================
# Squad table
# =========================

POSITION_FILTER_ORDER = ["GK", "CB", "FB", "DM", "CM", "AM", "WF", "CF"]


def render_squad_filters(
    df: pd.DataFrame,
    position_col: str = "common_position",
    nationality_col: str = "birth_country",
    age_col: str = "age",
    key_prefix: str = "squad",
) -> tuple[list[str], str]:
    position_counts = df[position_col].value_counts().to_dict()

    available_positions = [
        pos for pos in POSITION_FILTER_ORDER
        if pos in position_counts
    ]

    available_nationalities = (
        df[nationality_col]
        .dropna()
        .astype(str)
        .sort_values()
        .unique()
        .tolist()
    )

    valid_ages = df[age_col].dropna()
    if valid_ages.empty:
        min_age = 13
        max_age = 50
    else:
        min_age = int(valid_ages.min())
        max_age = int(valid_ages.max())

    title_col, positions_col, nationality_ui_col, age_ui_col = st.columns(
        [1.3, 5.7, 1.8, 1.8],
        vertical_alignment="center",
    )

    with title_col:
        st.markdown("## Squad")

    selected_positions = []

    with positions_col:
        if available_positions:
            filter_cols = st.columns(len(available_positions))

            for col, position in zip(filter_cols, available_positions):
                label = f"{position} ({position_counts[position]})"

                with col:
                    is_selected = st.checkbox(
                        label,
                        value=True,
                        key=f"{key_prefix}_position_{position}",
                    )

                    if is_selected:
                        selected_positions.append(position)

    with nationality_ui_col:
        selected_nationality = st.selectbox(
            "Nationality",
            options=["All"] + available_nationalities,
            index=0,
            key=f"{key_prefix}_nationality",
        )

    with age_ui_col:
        selected_age_range = st.slider(
            "Age",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age),
            step=1,
            key=f"{key_prefix}_age_range",
        )

    return selected_positions, selected_nationality, selected_age_range

squad_columns = [
    player_col,
    nationality_col,
    position_col,
    age_col,
    minutes_col,
    season_col,
    league_col,
    team_col,
    "on_loan",
    "team",
    "matches_played",
    "goals",
    "assists",
    "xg",
    "xa",
]

POSITION_TO_ROLE = {
        "GK": "GK",

        "CB": "CB",
        "LCB": "CB",
        "RCB": "CB",

        "LB": "FB",
        "RB": "FB",
        "LWB": "FB",
        "RWB": "FB",

        "DMF": "DM",
        "LDMF": "DM",
        "RDMF": "DM",

        "CMF": "CM",
        "LCMF": "CM",
        "RCMF": "CM",

        "AMF": "AM",

        "LAMF": "WF",
        "RAMF": "WF",
        "LW": "WF",
        "RW": "WF",
        "LWF": "WF",
        "RWF": "WF",

        "CF": "CF",
    }

squad_df = data_loader.build_squad_df(
    team_df=team_df,
    squad_columns=squad_columns,
    player_col="player",
    minutes_col="minutes_played",
    position_col="position",
    current_team_col="team_within_selected_timeframe",
    original_team_col="team",
)

filtered_squad_df = components.filter_players(
    squad_df=squad_df,
    position_col="common_position",
    nationality_col="birth_country",
    age_col="age",
    key_prefix="players",
)


components.render_team_players_list(
    players_df=filtered_squad_df,
    default_sort_col="Player",
    show_current_team=False,
)