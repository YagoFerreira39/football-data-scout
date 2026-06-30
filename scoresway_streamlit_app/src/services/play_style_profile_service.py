# =========================
# PLAY STYLE PROFILE SERVICE
# =========================

import pandas as pd

from src.domain.play_style_profile import (
    add_play_style_profile_scores,
    build_league_play_style_distribution,
    build_team_play_style_profile,
)
from src.domain.team_profile import get_available_team_options


def get_play_style_profile_dataframe(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Returns dataframe with play-style profile scores added.
    """

    return add_play_style_profile_scores(df)


def get_play_style_profile_team_options(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Returns team options for play-style profile selection.
    """

    return get_available_team_options(df)


def get_selected_team_play_style_profile(
    df: pd.DataFrame,
    *,
    team_option_label: str,
) -> pd.DataFrame:
    """
    Returns chart-ready play-style profile data for one team.
    """

    return build_team_play_style_profile(
        df,
        team_option_label=team_option_label,
    )

def get_league_play_style_distribution(
    df: pd.DataFrame,
    *,
    team_option_label: str,
) -> pd.DataFrame:
    """
    Returns league distribution data for the play-style chart.
    """

    return build_league_play_style_distribution(
        df,
        team_option_label=team_option_label,
    )

