# =========================
# TEAM STYLE SERVICE
# =========================

import pandas as pd

from src.domain.team_style import (
    build_team_style_profile,
    prepare_team_style_df,
)


def get_team_style_dataframe(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Returns the team stats dataframe with style scores added.
    """

    return prepare_team_style_df(df)


def get_selected_team_style_profile(
    df: pd.DataFrame,
    *,
    team_name: str,
    league_name: str,
    season: str,
) -> dict[str, pd.DataFrame]:
    """
    Builds the style profile for the selected team.
    """

    return build_team_style_profile(
        df,
        team_name=team_name,
        league_name=league_name,
        season=season,
    )