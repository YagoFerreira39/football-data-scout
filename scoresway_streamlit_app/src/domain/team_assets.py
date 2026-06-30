# =========================
# TEAM ASSETS DOMAIN LOGIC
# =========================

import pandas as pd

from src.config.team_assets import (
    TEAM_BADGE_LG_COLUMN,
    TEAM_BADGE_LG_TEMPLATE,
    TEAM_BADGE_SM_COLUMN,
    TEAM_BADGE_SM_TEMPLATE,
)


def _get_contestant_id_column(df: pd.DataFrame) -> str | None:
    """
    Finds the team ID column used to build badge URLs.
    """

    possible_columns = [
        "contestant_id",
        "contestantId",
        "contestantId".lower(),
    ]

    for col in possible_columns:
        if col in df.columns:
            return col

    return None


def add_team_badge_urls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds badge URL columns if they are missing.

    If badge_sm and badge_lg already exist from the scraper,
    they are preserved.
    """

    df = df.copy()

    contestant_id_col = _get_contestant_id_column(df)

    if contestant_id_col is None:
        return df

    contestant_ids = df[contestant_id_col].astype(str)

    if TEAM_BADGE_SM_COLUMN not in df.columns:
        df[TEAM_BADGE_SM_COLUMN] = contestant_ids.apply(
            lambda contestant_id: TEAM_BADGE_SM_TEMPLATE.format(
                contestant_id=contestant_id,
            )
        )

    if TEAM_BADGE_LG_COLUMN not in df.columns:
        df[TEAM_BADGE_LG_COLUMN] = contestant_ids.apply(
            lambda contestant_id: TEAM_BADGE_LG_TEMPLATE.format(
                contestant_id=contestant_id,
            )
        )

    return df