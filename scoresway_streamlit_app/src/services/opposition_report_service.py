# =========================
# OPPOSITION REPORT SERVICE
# =========================

from typing import Any

import pandas as pd

from src.domain.opposition_report import build_opposition_report
from src.domain.team_profile import get_available_team_options


def get_opposition_team_options(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Returns opponent options for the current filtered dataframe.
    """

    return get_available_team_options(df)


def get_selected_opposition_report(
    df: pd.DataFrame,
    *,
    team_option_label: str,
) -> dict[str, Any]:
    """
    Builds the selected opposition report helper.
    """

    return build_opposition_report(
        df,
        team_option_label=team_option_label,
    )