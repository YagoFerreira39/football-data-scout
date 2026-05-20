from pathlib import Path
from urllib.parse import urlencode
import re

import numpy as np
import pandas as pd
import streamlit as st

from config.theme import apply_theme
from src import league_map
from src.wyscout_data_loader import WyscoutDataLoader
from components.components import Components
from src.ratings.player_ratings import build_player_ratings_table
from src.ratings.rating_profiles import RATING_PROFILE_OPTIONS


st.set_page_config(
    page_title="Competition | RoleRadar",
    page_icon="⚽",
    layout="wide",
)
apply_theme()

components = Components()

country_col = "league_country"
league_col = "league_name"
season_col = "season"
team_col = "team_within_selected_timeframe"
player_col = "player"

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

@st.cache_data(show_spinner="Calculating player ratings...")
def calculate_role_ratings(
    df: pd.DataFrame,
    selected_league: str,
    selected_season: str,
    selected_rating_profile_label: str,
    minimum_minutes_played: int = 1000,
) -> pd.DataFrame:
    selected_rating_profile = RATING_PROFILE_OPTIONS[selected_rating_profile_label]

    ratings_df = build_player_ratings_table(
        df=df,
        league_name=selected_league,
        season=selected_season,
        positions=selected_rating_profile["positions"],
        category_weights=selected_rating_profile["category_weights"],
        feature_weights=selected_rating_profile["feature_weights"],
        minimum_minutes_played=minimum_minutes_played,
    )

    return ratings_df

df = load_data()

# =========================
# Helpers
# =========================

def slugify(value: str) -> str:
    value = str(value).lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")

# Sidebar filters
selected_country, selected_league, selected_season, team_search, player_search, selected_rating_profile_label, minimum_minutes_played = (
    components.render_sidebar_filters(
        df=df,
        country_col=country_col,
        league_col=league_col,
        season_col=season_col,
        key_prefix="leagues",
    )
)

# =========================
# Read selected context
# =========================
query_params = st.query_params

country_slug = query_params.get("country")
league_slug = query_params.get("league")

selected_country = st.session_state.get("selected_country")
selected_league = st.session_state.get("selected_league")

if selected_country and selected_league:
    competition_df = df[
        (df[country_col] == selected_country)
        & (df[league_col] == selected_league)
    ].copy()

elif country_slug and league_slug:
    df["country_slug"] = df[country_col].apply(slugify)
    df["league_slug"] = df[league_col].apply(slugify)

    competition_df = df[
        (df["country_slug"] == country_slug)
        & (df["league_slug"] == league_slug)
    ].copy()

    if competition_df.empty:
        st.error("No data found for the selected league.")
        st.stop()

    selected_country = competition_df[country_col].iloc[0]
    selected_league = competition_df[league_col].iloc[0]

    st.session_state["selected_country"] = selected_country
    st.session_state["selected_league"] = selected_league

else:
    st.warning("No competition selected. Go back to the main page and select a competition.")
    st.stop()

st.markdown(
    f"""
    <div class="team-header">
        <div class="team-header-title">{selected_league}</div>
        <div class="team-header-meta">
            <span class="team-header-pill">{selected_country}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


competition_df = df[
    (df[country_col] == selected_country)
    & (df[league_col] == selected_league)
].copy()


available_seasons = sorted(
    competition_df[season_col].dropna().unique(),
    reverse=True,
)

selected_season = st.segmented_control(
    "Season",
    options=available_seasons,
    default=available_seasons[0],
)

season_competition_df = competition_df[
    competition_df[season_col] == selected_season
]

def build_team_url(
    country: str,
    league: str,
    season: str,
    team: str,
) -> str:
    query_params = urlencode(
        {
            "country": slugify(country),
            "league": slugify(league),
            "season": slugify(season),
            "team": slugify(team),
        }
    )

    return f"/teams?{query_params}"

teams_source_df = season_competition_df.copy()

if team_search:
    teams_source_df = teams_source_df[
        teams_source_df[team_col].str.contains(
            team_search,
            case=False,
            na=False,
        )
    ]

if player_search:
    teams_source_df = teams_source_df[
        teams_source_df[player_col].str.contains(
            player_search,
            case=False,
            na=False,
        )
    ]

available_teams_df = (
    teams_source_df[[team_col, league_col, country_col, season_col]]
    .drop_duplicates()
    .sort_values([team_col, league_col])
    .reset_index(drop=True)
)

st.subheader("Available Teams")

components.render_teams_grid(
    teams_df=available_teams_df,
    team_col=team_col,
    league_col=league_col,
    country_col=country_col,
    season_col=season_col,
)

squad_columns = [
    "player",
    "birth_country",
    "position",
    "age",
    "minutes_played",
    "matches_played",
    "goals",
    "assists",
    "xg",
    "xa",
    "team",
    "team_within_selected_timeframe",
    "on_loan",
    "season",
]
squad_df = data_loader.build_squad_df(
    team_df=season_competition_df,
    squad_columns=squad_columns,
    player_col="player",
    minutes_col="minutes_played",
    position_col="position",
    current_team_col="team_within_selected_timeframe",
    original_team_col="team",
)
filtered_squad_df = squad_df.copy()

st.divider()

# filtered_squad_df = components.filter_players(
#     squad_df=squad_df,
#     position_col="common_position",
#     nationality_col="birth_country",
#     age_col="age",
#     key_prefix="league_players",
# )

# components.render_team_players_list(
#     players_df=filtered_squad_df,
#     default_sort_col="Player",
# )

# 
# selected_rating_profile = RATING_PROFILE_OPTIONS[selected_rating_profile_label]

# ratings_df = build_player_ratings_table(
#     df=competition_df,
#     league_name=selected_league,
#     season=selected_season,
#     positions=selected_rating_profile["positions"],
#     category_weights=selected_rating_profile["category_weights"],
#     feature_weights=selected_rating_profile["feature_weights"],
#     minimum_minutes_played=1000,
# )


ratings_df = calculate_role_ratings(
    df=competition_df,
    selected_league=selected_league,
    selected_season=selected_season,
    selected_rating_profile_label=selected_rating_profile_label,
    minimum_minutes_played=minimum_minutes_played,
)

st.markdown(f"## Player Ratings - {selected_rating_profile_label}")

if ratings_df.empty:
    st.info("No players found for the selected rating profile and minimum minutes.")
else:
    components.render_player_ratings_list(
        ratings_df=ratings_df,
        title=f"",
        # default_sort_col="overall_rating",
        # sort_state_prefix="league_ratings",
    )
    # st.dataframe(
    #     ratings_df,
    #     use_container_width=True,
    #     hide_index=True,
    #     column_config={
    #         "rank": st.column_config.NumberColumn("Rank", format="%d"),
    #         "player": st.column_config.TextColumn("Player"),
    #         "team_within_selected_timeframe": st.column_config.TextColumn("Team"),
    #         "main_position": st.column_config.TextColumn("Position"),
    #         "age": st.column_config.NumberColumn("Age", format="%d"),
    #         "minutes_played": st.column_config.NumberColumn("Minutes", format="%d"),
    #         "overall_rating": st.column_config.NumberColumn("Overall", format="%.2f"),
    #     },
    # )