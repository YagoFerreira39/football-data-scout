# =========================
# SIMILAR TEAMS DOMAIN LOGIC
# =========================

import numpy as np
import pandas as pd

from src.config.similar_teams import (
    SIMILAR_TEAM_SCORE_COLUMNS,
    SIMILAR_TEAMS_OUTPUT_COLUMNS,
)
from src.domain.team_profile import select_team_row_by_option


def _get_available_similarity_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> list[str]:
    """
    Returns style score columns available in the dataframe.
    """

    return [col for col in columns if col in df.columns]


def _filter_candidate_pool(
    df: pd.DataFrame,
    reference_row: pd.Series,
    *,
    candidate_scope: str,
) -> pd.DataFrame:
    """
    Filters candidate teams according to the selected comparison scope.
    """

    candidates = df.copy()

    if candidate_scope == "same_league_season":
        candidates = candidates[
            (candidates["source_league_slug"] == reference_row["source_league_slug"])
            & (candidates["source_season"] == reference_row["source_season"])
        ]

    elif candidate_scope == "same_country_season":
        candidates = candidates[
            (candidates["source_country_name"] == reference_row["source_country_name"])
            & (candidates["source_season"] == reference_row["source_season"])
        ]

    elif candidate_scope == "same_season":
        candidates = candidates[
            candidates["source_season"] == reference_row["source_season"]
        ]

    elif candidate_scope == "all":
        candidates = candidates.copy()

    else:
        raise ValueError(f"Unknown candidate scope: {candidate_scope}")

    return candidates


def _remove_reference_team(
    candidates: pd.DataFrame,
    reference_row: pd.Series,
) -> pd.DataFrame:
    """
    Removes the selected team from the candidate pool.
    """

    return candidates[
        ~(
            (candidates["contestant_name"] == reference_row["contestant_name"])
            & (candidates["source_league_slug"] == reference_row["source_league_slug"])
            & (candidates["source_season"] == reference_row["source_season"])
        )
    ].copy()


def calculate_style_similarity(
    candidates: pd.DataFrame,
    reference_row: pd.Series,
    *,
    columns: list[str],
) -> pd.DataFrame:
    """
    Calculates style similarity using Euclidean distance.

    Lower distance means more similar.
    Higher similarity_score means more similar.
    """

    if candidates.empty:
        raise ValueError("No candidate teams available for similarity search.")

    available_cols = _get_available_similarity_columns(
        candidates,
        columns,
    )

    if not available_cols:
        raise ValueError("No valid style score columns available for similarity search.")

    candidates = candidates.dropna(
        subset=available_cols,
        how="all",
    ).copy()

    if candidates.empty:
        raise ValueError("Candidate teams have no style score values.")

    candidate_matrix = candidates[available_cols].astype(float)

    column_means = candidate_matrix.mean().fillna(50)

    candidate_matrix = candidate_matrix.fillna(column_means)

    reference_vector = (
        reference_row[available_cols]
        .astype(float)
        .fillna(column_means)
    )

    distances = np.sqrt(
        ((candidate_matrix - reference_vector) ** 2).sum(axis=1)
    )

    max_possible_distance = np.sqrt(len(available_cols) * (100 ** 2))

    similarity_score = (
        100 * (1 - distances / max_possible_distance)
    ).clip(lower=0, upper=100)

    result = candidates.copy()
    result["style_distance"] = distances
    result["similarity_score"] = similarity_score

    return result


def find_similar_teams(
    df: pd.DataFrame,
    *,
    reference_team_option_label: str,
    candidate_scope: str = "same_season",
    top_n: int = 10,
    columns: list[str] = SIMILAR_TEAM_SCORE_COLUMNS,
) -> pd.DataFrame:
    """
    Finds teams with the most similar team style profile.

    This compares style identity, not team quality.
    """

    if df.empty:
        raise ValueError("Cannot find similar teams from an empty dataframe.")

    reference_row = select_team_row_by_option(
        df,
        team_option_label=reference_team_option_label,
    )

    candidates = _filter_candidate_pool(
        df,
        reference_row,
        candidate_scope=candidate_scope,
    )

    candidates = _remove_reference_team(
        candidates,
        reference_row,
    )

    result = calculate_style_similarity(
        candidates,
        reference_row,
        columns=columns,
    )

    available_output_cols = [
        col for col in SIMILAR_TEAMS_OUTPUT_COLUMNS
        if col in result.columns
    ]

    available_score_cols = [
        col for col in columns
        if col in result.columns
    ]

    return (
        result[available_output_cols + available_score_cols]
        .sort_values(
            ["similarity_score", "style_distance"],
            ascending=[False, True],
        )
        .head(top_n)
        .reset_index(drop=True)
    )