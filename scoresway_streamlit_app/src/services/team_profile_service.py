# =========================
# TEAM PROFILE SERVICE
# =========================

import pandas as pd

from src.domain.team_profile import (
    build_team_profile,
    get_available_team_options,
)


def get_team_options(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Returns team options for the current filtered dataframe.
    """

    return get_available_team_options(df)


def get_selected_team_profile(
    df: pd.DataFrame,
    *,
    team_option_label: str,
) -> dict[str, pd.DataFrame]:
    """
    Builds the selected team profile.
    """

    return build_team_profile(
        df,
        team_option_label=team_option_label,
    )