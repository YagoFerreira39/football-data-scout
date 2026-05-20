from html import escape
from textwrap import dedent

import pandas as pd
import streamlit as st

from src.wyscout_data_loader import WyscoutDataLoader
from components.players_components import render_detailed_stats, render_player_bio_strip, render_player_header


# =========================
# Constants
# =========================

player_col = "player"
team_col = "team_within_selected_timeframe"
season_col = "season"
league_col = "league_name"
country_col = "league_country"
position_col = "position"
common_position_col = "common_position"
age_col = "age"
birth_country_col = "birth_country"
passport_country_col = "passport_country"
foot_col = "foot"
height_col = "height"
weight_col = "weight"
contract_col = "contract_expires"
loan_col = "on_loan"

PLAYER_PROFILE_OPTIONS = {
    "Default": "default",
    # AM
    "Attacking Midfielder": "attacking_midfielder",
    # CB
    "Ball-Playing CB": "ball_playing",
    "Aerially Dominant CB": "aerially_dominant",
    # FB    
    "Defensive Fullback": "defensive_fullback",
    "Attacking Fullback": "attacking_fullback",
    "Inverted Fullback": "inverted_fullback",
    "Wing-Back": "wing_back",
    # CM
    "Ball-Winning Midfielder": "ball_winning_midfielder",
    "Ball-Playing Midfielder": "ball_playing_midfielder",
    "Box-to-Box Midfielder": "box_to_box",
    # W
    "Touchline Winger": "touchline_winger",
    "Half-Space Drifter": "half_space_drifter",
    "Inside Forward": "inside_forward_winger",
    # CF
    "Mobile / Run Behind CF": "mobile_run_behind",
    "Target Man": "target_man",
}

PROFILE_OPTIONS_BY_POSITION_GROUP = {
    "GK": [
        "Default",
    ],

    "CB": [
        "Default",
        "Ball-Playing CB",
        "Aerially Dominant CB",
    ],

    "FB": [
        "Default",
        "Defensive Fullback",
        "Attacking Fullback",
        "Inverted Fullback",
        "Wing-Back",
    ],

    "CM_DM": [
        "Default",
        "Ball-Winning Midfielder",
        "Ball-Playing Midfielder",
        "Box-to-Box Midfielder",
    ],

    "AM": [
        "Default",
        "Attacking Midfielder",
    ],

    "WINGER": [
        "Default",
        "Touchline Winger",
        "Half-Space Drifter",
        "Inside Forward",
    ],

    "CF": [
        "Default",
        "Mobile / Run Behind CF",
        "Target Man",
    ],
}

SCATTER_METRIC_OPTIONS = {
    "Shooting Volume vs Box Threat": {
        "x_metric": "shots_per_90",
        "y_metric": "touches_in_box_per_90",
        "availability": "outfield",
    },
    "xG vs Goals": {
        "x_metric": "xg_per_90",
        "y_metric": "goals_per_90",
        "availability": "outfield",
    },
    "Chance Creation vs xA": {
        "x_metric": "key_passes_per_90",
        "y_metric": "xa_per_90",
        "availability": "outfield",
    },
    "Progressive Passing vs Accuracy": {
        "x_metric": "progressive_passes_per_90",
        "y_metric": "accurate_progressive_passes_%",
        "availability": "all",
    },
    "Final Third Passing vs Penalty Area Passing": {
        "x_metric": "passes_to_final_third_per_90",
        "y_metric": "passes_to_penalty_area_per_90",
        "availability": "outfield",
    },
    "Passing Volume vs Pass Accuracy": {
        "x_metric": "passes_per_90",
        "y_metric": "accurate_passes_%",
        "availability": "all",
    },
    "Dribbling Volume vs Success": {
        "x_metric": "dribbles_per_90",
        "y_metric": "successful_dribbles_%",
        "availability": "outfield",
    },
    "Ball Carrying vs Accelerations": {
        "x_metric": "progressive_runs_per_90",
        "y_metric": "accelerations_per_90",
        "availability": "outfield",
    },
    "Defensive Duels vs Duel Success": {
        "x_metric": "defensive_duels_per_90",
        "y_metric": "defensive_duels_won_%",
        "availability": "outfield",
    },
    "Aerial Duels vs Aerial Success": {
        "x_metric": "aerial_duels_per_90",
        "y_metric": "aerial_duels_won_%",
        "availability": "outfield",
    },
    "Interceptions vs Defensive Actions": {
        "x_metric": "interceptions_per_90",
        "y_metric": "successful_defensive_actions_per_90",
        "availability": "outfield",
    },
    "GK Shot-Stopping": {
        "x_metric": "shots_against_per_90",
        "y_metric": "save_rate_%",
        "availability": "gk",
    },
}

# =========================
# Query params
# =========================

query_params = st.query_params

player_slug = query_params.get("player")
team_slug = query_params.get("team")
season_slug = query_params.get("season")

if not player_slug or not team_slug or not season_slug:
    st.title("Players")
    st.info("Select a player from a team page to view the player profile.")
    st.stop()


# =========================
# Load data
# =========================

data_loader = WyscoutDataLoader()

@st.cache_data
def load_player_data(
    player: str, 
    team: str, 
    # season: str
) -> pd.DataFrame:
    return data_loader.build_player_df(
        player=player,
        team=team,
        # season=season,
    )
    
player_all_seasons_df = load_player_data(
    player=player_slug,
    team=team_slug,
)

if player_all_seasons_df.empty:
    st.error("No data found for the selected player.")
    st.write(
        {
            "player": player_slug,
            "team": team_slug,
        }
    )
    st.stop()
    
available_seasons = sorted(
    player_all_seasons_df[season_col]
    .dropna()
    .astype(str)
    .unique()
    .tolist(),
    reverse=True,
)

if not available_seasons:
    st.error("No seasons found for the selected player.")
    st.stop()
    
selected_season = None

if season_slug:
    selected_season = next(
        (
            season
            for season in available_seasons
            if data_loader.slugify(season) == season_slug
        ),
        None,
    )
    
default_season = selected_season or available_seasons[0]

if selected_season is None:
    selected_season = available_seasons[0]

# # =========================
# # Helpers
# # =========================

def update_player_season_query_params() -> None:
    st.query_params["player"] = player_slug
    st.query_params["team"] = team_slug
    st.query_params["season"] = data_loader.slugify(st.session_state["player_selected_season"])
    
def get_player_position(player_row: pd.Series) -> str:
    position = player_row.get("main_position")

    if pd.isna(position) or not str(position).strip():
        position = player_row.get("position")

    if pd.isna(position):
        return ""

    return str(position).strip().upper()
    
def get_position_group(position: str) -> str:
    if position in {"GK"}:
        return "GK"

    if position in {"CB", "CCB", "LCB", "RCB"}:
        return "CB"

    if position in {"LB", "LWB", "RB", "RWB"}:
        return "FB"

    if position in {"DMF", "LDMF", "RDMF", "LCMF", "RCMF"}:
        return "CM_DM"

    if position in {"AMF"}:
        return "AM"

    if position in {"LW", "LWF", "LAMF", "RW", "RWF", "RAMF"}:
        return "WINGER"

    if position in {"CF"}:
        return "CF"

    return "DEFAULT"

def get_available_profile_options(player_row: pd.Series) -> dict[str, str | None]:
    position = get_player_position(player_row)
    position_group = get_position_group(position)

    allowed_labels = PROFILE_OPTIONS_BY_POSITION_GROUP.get(
        position_group,
        ["Default"],
    )

    return {
        label: PLAYER_PROFILE_OPTIONS[label]
        for label in allowed_labels
        if label in PLAYER_PROFILE_OPTIONS
    }

def available_scatter_metrics(
    player_row: pd.Series,
    scatter_metrics: dict,
) -> dict:
    available_metrics = {}
    player_is_gk = bool(player_row["position"] == "GK")

    for label, config in scatter_metrics.items():
        availability = config.get("availability", "all")

        if availability == "all":
            available_metrics[label] = config

        elif availability == "gk" and player_is_gk:
            available_metrics[label] = config

        elif availability == "outfield" and not player_is_gk:
            available_metrics[label] = config

    return available_metrics

# LOAD PLAYER_DF    
player_df = player_all_seasons_df[
    player_all_seasons_df[season_col].astype(str).eq(str(selected_season))
].copy()

if player_df.empty:
    st.error("No data found for the selected season.")
    st.stop()

player = player_df.iloc[0]
league_df = data_loader.build_league_season_df_from_player(player_row=player)
league_season_df = league_df[league_df["season"] == player["season"]]
available_profile_options = get_available_profile_options(player)
available_scatter_options = available_scatter_metrics(
    player_row=player,
    scatter_metrics=SCATTER_METRIC_OPTIONS,
)

# =========================
# Header
# =========================

with st.sidebar:
    st.markdown("### Player Filters")

    selected_season = st.segmented_control(
        "Season",
        options=available_seasons,
        default=selected_season,
        key="player_selected_season",
        on_change=update_player_season_query_params,
    )

    selected_profile_label = st.selectbox(
        "Player profile - Charts",
        options=list(available_profile_options.keys()),
        index=0,
        key="player_selected_profile",
    )
    
    selected_scatter_label = st.selectbox(
        "Comparison Options - Scatter chart",
        options=list(available_scatter_options.keys()),
        index=0,
        key="player_selected_scatter_chart",
    )
    min_minutes_default = 500 if player["minutes_played"] < 1000 else 1000
    minimum_minutes_played = st.sidebar.number_input(
        "Minimum Minutes",
        min_value=0,
        max_value=5000,
        value=min_minutes_default,
        step=100,
        key="player_selected_min_minutes",
    )
    
selected_profile = available_profile_options[selected_profile_label]
selected_scatter_metrics = SCATTER_METRIC_OPTIONS[selected_scatter_label]
selected_x_metric = selected_scatter_metrics["x_metric"]
selected_y_metric = selected_scatter_metrics["y_metric"]

render_player_header(player_row=player, selected_season=selected_season)

render_player_bio_strip(player_row=player)

render_detailed_stats(
    player_row=player, 
    league_season_df=league_season_df, 
    league_df=league_df, 
    selected_profile=selected_profile,
    selected_scatter_metrics=selected_scatter_metrics,
    minimum_minutes_played=minimum_minutes_played
)

# =========================