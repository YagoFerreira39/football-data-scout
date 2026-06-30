# =========================
# SIMILAR TEAMS SERVICE
# =========================

import pandas as pd

from src.domain.similar_teams import find_similar_teams
from src.domain.team_profile import get_available_team_options


def get_similar_team_reference_options(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Returns reference team options for the current filtered dataframe.
    """

    return get_available_team_options(df)


def get_similar_teams(
    df: pd.DataFrame,
    *,
    reference_team_option_label: str,
    candidate_scope: str,
    top_n: int,
) -> pd.DataFrame:
    """
    Returns the most similar teams to the selected reference team.
    """

    return find_similar_teams(
        df,
        reference_team_option_label=reference_team_option_label,
        candidate_scope=candidate_scope,
        top_n=top_n,
    )