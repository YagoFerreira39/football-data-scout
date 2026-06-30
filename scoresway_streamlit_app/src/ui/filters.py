# =========================
# FILTER UI
# =========================

import pandas as pd
import streamlit as st

from src.services.team_stats_service import filter_team_stats


def render_league_filters(
    team_stats_df: pd.DataFrame,
    available_leagues_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Render country, league and season filters.
    Return the filtered team stats dataframe.
    """

    st.subheader("Select League")

    col1, col2, col3 = st.columns(3)

    with col1:
        countries = ["All"] + sorted(
            available_leagues_df["source_country_name"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_country = st.selectbox(
            "Country",
            countries,
        )

    league_options_df = available_leagues_df.copy()

    if selected_country != "All":
        league_options_df = league_options_df[
            league_options_df["source_country_name"] == selected_country
        ]

    with col2:
        leagues = ["All"] + sorted(
            league_options_df["source_league_name"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_league = st.selectbox(
            "League",
            leagues,
        )

    season_options_df = league_options_df.copy()

    if selected_league != "All":
        season_options_df = season_options_df[
            season_options_df["source_league_name"] == selected_league
        ]

    with col3:
        seasons = ["All"] + sorted(
            season_options_df["source_season"]
            .dropna()
            .unique()
            .tolist(),
            reverse=True,
        )

        selected_season = st.selectbox(
            "Season",
            seasons,
        )

    return filter_team_stats(
        team_stats_df,
        country_name=selected_country,
        league_name=selected_league,
        season=selected_season,
    )