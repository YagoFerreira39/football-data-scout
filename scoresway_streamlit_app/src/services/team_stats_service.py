# =========================
# TEAM STATS SERVICE
# =========================

import pandas as pd

from src.domain.team_assets import add_team_badge_urls
from src.config.columns import AVAILABLE_LEAGUES_COLUMNS
from src.data.loader import load_team_stats_files
from src.domain.team_metrics import add_team_derived_metrics
from src.domain.team_style import prepare_team_style_df
from src.domain.play_style_profile import add_play_style_profile_scores


def get_team_stats_data(
    data_dir: str = "data/processed",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load team stats, add team assets, add derived metrics,
    add style scores, add play-style profile scores and return available leagues.
    """

    team_stats_df = load_team_stats_files(data_dir)

    team_stats_df = add_team_badge_urls(team_stats_df)

    team_stats_df = add_team_derived_metrics(team_stats_df)

    team_stats_df = prepare_team_style_df(team_stats_df)

    team_stats_df = add_play_style_profile_scores(team_stats_df)

    available_leagues_df = get_available_leagues(team_stats_df)

    return team_stats_df, available_leagues_df


def get_available_leagues(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return one row per available league-season.
    """

    available_cols = [
        col for col in AVAILABLE_LEAGUES_COLUMNS
        if col in df.columns
    ]

    return (
        df[available_cols]
        .drop_duplicates()
        .sort_values(available_cols)
        .reset_index(drop=True)
    )


def filter_team_stats(
    df: pd.DataFrame,
    *,
    country_name: str | None = None,
    league_name: str | None = None,
    season: str | None = None,
) -> pd.DataFrame:
    """
    Filter team stats by country, league and season.
    """

    view = df.copy()

    if country_name and country_name != "All":
        view = view[view["source_country_name"] == country_name]

    if league_name and league_name != "All":
        view = view[view["source_league_name"] == league_name]

    if season and season != "All":
        view = view[view["source_season"] == season]

    return view.reset_index(drop=True)