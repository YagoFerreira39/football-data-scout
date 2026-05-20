from html import escape
from pathlib import Path
import re
from urllib.parse import urlencode

import numpy as np
import pandas as pd
import streamlit as st

from config.theme import apply_theme
from src import league_map
from src.wyscout_data_loader import WyscoutDataLoader
from components.components import Components


# =========================
# Constants
# =========================
data_loader = WyscoutDataLoader()
components = Components()
COLUMN_MAP = {
    "league_country": "league_country",
    "league_base": "league_name",
    "season": "season",
    "player": "player",
    "player_birth_country": "birth_country",
    "team": "team_within_selected_timeframe",
    "main_position": "main_position",
    "minutes": "minutes_played",
}

required_columns = [
    COLUMN_MAP["league_country"],
    COLUMN_MAP["league_base"],
    COLUMN_MAP["season"],
    COLUMN_MAP["player"],
]

PRIORITY_LEAGUES = [
    "Premier League",
    "La Liga",
    "Serie A",
    "Bundesliga",
    "Ligue 1",
    "Primeira Liga",
    "Eredivisie",
    "Belgian Pro League",
    "Campeonato Brasileiro Série A",
    "Campeonato Brasileiro Série B",
    "Major League Soccer",
    "EFL Championship",
    "Scottish Premiership",
    "Süper Lig",
    "2. Bundesliga",
]

PRIORITY_LEAGUE_ORDER = {
    league: index for index, league in enumerate(PRIORITY_LEAGUES)
}

# =========================
# Helpers
# =========================

def slugify(value: str) -> str:
    value = str(value).lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")

def validate_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(
            "Missing required columns in the CSV: "
            + ", ".join(missing_columns)
        )
        st.stop()
        
def filter_dataframe(
    df: pd.DataFrame,
    selected_country: str | None,
    selected_league: str | None,
    selected_season: str | None,
    player_search: str,
    team_search: str,
) -> pd.DataFrame:
    filtered_df = df.copy()

    country_col = COLUMN_MAP["league_country"]
    league_col = COLUMN_MAP["league_base"]
    season_col = COLUMN_MAP["season"]
    player_col = COLUMN_MAP["player"]
    team_col = COLUMN_MAP["team"]

    if selected_country and selected_country != "All":
        filtered_df = filtered_df[filtered_df[country_col] == selected_country]

    if selected_league and selected_league != "All":
        filtered_df = filtered_df[filtered_df[league_col] == selected_league]

    if selected_season and selected_season != "All":
        filtered_df = filtered_df[filtered_df[season_col] == selected_season]

    if player_search:
        filtered_df = filtered_df[
            filtered_df[player_col].str.contains(
                player_search,
                case=False,
                na=False,
            )
        ]

    if team_search:
        filtered_df = filtered_df[
            filtered_df[team_col].str.contains(
                team_search,
                case=False,
                na=False,
            )
        ]

    return filtered_df

# =========================
# Data loading
# =========================

@st.cache_data
def load_data() -> pd.DataFrame:
    df = data_loader.prepare_wyscout_data()
    df.columns = df.columns.str.strip()

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    return df

df = load_data()
validate_columns(df, required_columns)
df = df[df["league_base"].isin(league_map.league_map.keys())].copy()


# =========================
# Sidebar filters
# =========================

st.sidebar.header("Filters")

country_col = COLUMN_MAP["league_country"]
league_col = COLUMN_MAP["league_base"]
season_col = COLUMN_MAP["season"]
player_col = COLUMN_MAP["player"]
player_birth_country_col = COLUMN_MAP["player_birth_country"]
team_col = COLUMN_MAP["team"]
position_col = COLUMN_MAP["main_position"]
minutes_col = COLUMN_MAP["minutes"]

selected_country, selected_league, selected_season, team_search, player_search, selected_rating_profile_label, minimum_minutes_played = (
    components.render_sidebar_filters(
        df=df,
        country_col=country_col,
        league_col=league_col,
        season_col=season_col,
        key_prefix="main",
    )
)


# =========================
# Apply filters
# =========================

filtered_df = filter_dataframe(
    df=df,
    selected_country=selected_country,
    selected_league=selected_league,
    selected_season=selected_season,
    player_search=player_search,
    team_search=team_search
)

# =========================
# Header
# =========================
# Render the header with KPI cards based on the filtered dataframe
components.render_main_header(
    filtered_df=filtered_df,
    country_col=country_col,
    league_col=league_col,
    team_col=team_col,
    player_col=player_col,
)

# =========================
# Country / League / Season overview
# =========================

st.subheader("Leagues")

competitions_df: pd.DataFrame = data_loader.filter_and_sort_leagues_df(
    filtered_df=filtered_df,
    league_col=league_col,
    country_col=country_col,
    season_col=season_col,
    priority_league_order=PRIORITY_LEAGUE_ORDER,
)

components.render_league_grid(
    leagues_df=competitions_df,
    league_col=league_col,
    country_col=country_col,
)

st.divider()

# =========================
# League / Season overview
# =========================

if selected_league != "All" or team_search != "":
    st.subheader("Teams")
    
    available_teams_df = (
        filtered_df[[team_col, league_col, country_col, season_col]]
        .drop_duplicates()
        .sort_values([team_col, season_col], ascending=[True, False])
        .drop_duplicates(subset=[team_col, league_col, country_col], keep="first")
        .sort_values([team_col, league_col, country_col])
        .reset_index(drop=True)
    )

    components.render_teams_grid(
        teams_df=available_teams_df,
        team_col=team_col,
        league_col=league_col,
        country_col=country_col,
        season_col=season_col,
    )


# =========================
# Player search results
# =========================


players_df = (
    filtered_df
    .groupby(
        [
            player_col,
            player_birth_country_col,
            team_col,
            league_col,
            position_col,
        ],
        as_index=False,
    )
    .agg({
        minutes_col: "sum",
    })
    .sort_values([player_col, team_col, league_col])
    .reset_index(drop=True)
)

# =========================
# Optional selected player block
# =========================

if selected_league != "All" or (player_search and not players_df.empty):
    st.divider()
    st.subheader("Matched Players")
    
    components.render_players_list(
        players_df=players_df,
        default_sort_col="Player",
        show_minutes_played=False,
    )
