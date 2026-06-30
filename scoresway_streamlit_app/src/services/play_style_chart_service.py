# =========================
# PLAY STYLE CHART SERVICE
# =========================

import pandas as pd

from src.domain.play_style_chart import build_play_style_comparison
from src.domain.team_profile import get_available_team_options


def get_play_style_team_options(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Returns team options for play-style chart selectors.
    """

    return get_available_team_options(df)


def get_play_style_comparison_data(
    df: pd.DataFrame,
    *,
    team_option_label: str,
    comparison_type: str,
    comparison_team_option_label: str | None = None,
) -> pd.DataFrame:
    """
    Returns play-style comparison data for visualization.
    """

    return build_play_style_comparison(
        df,
        team_option_label=team_option_label,
        comparison_type=comparison_type,
        comparison_team_option_label=comparison_team_option_label,
    )