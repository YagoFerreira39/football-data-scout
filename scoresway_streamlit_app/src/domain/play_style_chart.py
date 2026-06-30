# =========================
# PLAY STYLE CHART DOMAIN LOGIC
# =========================

import pandas as pd

from src.config.play_style_chart import (
    PLAY_STYLE_CHART_LABELS,
    PLAY_STYLE_CHART_SCORE_COLUMNS,
)
from src.domain.team_profile import select_team_row_by_option


def _get_league_season_df(
    df: pd.DataFrame,
    team_row: pd.Series,
) -> pd.DataFrame:
    """
    Returns all teams from the selected team's league-season.
    """

    mask = (
        (df["source_league_slug"] == team_row["source_league_slug"])
        & (df["source_season"] == team_row["source_season"])
    )

    return df[mask].copy()


def _get_available_score_columns(
    df: pd.DataFrame,
) -> list[str]:
    """
    Returns available play-style score columns.
    """

    return [
        col for col in PLAY_STYLE_CHART_SCORE_COLUMNS
        if col in df.columns
    ]


def build_league_average_comparison(
    df: pd.DataFrame,
    *,
    team_option_label: str,
) -> pd.DataFrame:
    """
    Builds a play-style comparison table:
    selected club vs league average.
    """

    team_row = select_team_row_by_option(
        df,
        team_option_label=team_option_label,
    )

    league_df = _get_league_season_df(
        df,
        team_row,
    )

    score_cols = _get_available_score_columns(df)

    rows = []

    for col in score_cols:
        team_score = team_row[col]
        comparison_score = league_df[col].mean()

        rows.append(
            {
                "style_area": PLAY_STYLE_CHART_LABELS.get(col, col),
                "score_column": col,
                "team_name": team_row["contestant_name"],
                "comparison_name": "League average",
                "team_score": team_score,
                "comparison_score": comparison_score,
                "difference": team_score - comparison_score,
            }
        )

    return pd.DataFrame(rows)


def build_team_to_team_comparison(
    df: pd.DataFrame,
    *,
    team_option_label: str,
    comparison_team_option_label: str,
) -> pd.DataFrame:
    """
    Builds a play-style comparison table:
    selected club vs another selected club.
    """

    team_row = select_team_row_by_option(
        df,
        team_option_label=team_option_label,
    )

    comparison_row = select_team_row_by_option(
        df,
        team_option_label=comparison_team_option_label,
    )

    score_cols = _get_available_score_columns(df)

    rows = []

    for col in score_cols:
        team_score = team_row[col]
        comparison_score = comparison_row[col]

        rows.append(
            {
                "style_area": PLAY_STYLE_CHART_LABELS.get(col, col),
                "score_column": col,
                "team_name": team_row["contestant_name"],
                "comparison_name": comparison_row["contestant_name"],
                "team_score": team_score,
                "comparison_score": comparison_score,
                "difference": team_score - comparison_score,
            }
        )

    return pd.DataFrame(rows)


def build_play_style_comparison(
    df: pd.DataFrame,
    *,
    team_option_label: str,
    comparison_type: str,
    comparison_team_option_label: str | None = None,
) -> pd.DataFrame:
    """
    Builds the play-style comparison dataframe used by the chart.
    """

    if df.empty:
        raise ValueError("Cannot build play-style chart from an empty dataframe.")

    if comparison_type == "league_average":
        return build_league_average_comparison(
            df,
            team_option_label=team_option_label,
        )

    if comparison_type == "selected_team":
        if not comparison_team_option_label:
            raise ValueError("A comparison team must be selected.")

        return build_team_to_team_comparison(
            df,
            team_option_label=team_option_label,
            comparison_team_option_label=comparison_team_option_label,
        )

    raise ValueError(f"Unknown comparison type: {comparison_type}")