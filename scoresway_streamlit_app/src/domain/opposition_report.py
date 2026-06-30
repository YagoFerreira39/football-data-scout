# =========================
# OPPOSITION REPORT DOMAIN LOGIC
# =========================

from typing import Any

import pandas as pd

from src.config.opposition_report import (
    OPPOSITION_HIGH_SCORE_THRESHOLD,
    OPPOSITION_LOW_SCORE_THRESHOLD,
    OPPOSITION_STYLE_RULES,
)
from src.config.team_style import TEAM_STYLE_SCORE_LABELS
from src.domain.team_profile import (
    build_team_metric_groups,
    select_team_row_by_option,
)
from src.domain.team_style import build_team_style_profile


# =========================
# INTERNAL HELPERS
# =========================

def _score_band(score: float) -> str:
    """
    Converts a score into a high, medium or low band.
    """

    if pd.isna(score):
        return "unknown"

    if score >= OPPOSITION_HIGH_SCORE_THRESHOLD:
        return "high"

    if score <= OPPOSITION_LOW_SCORE_THRESHOLD:
        return "low"

    return "medium"


def _get_league_season_df(
    df: pd.DataFrame,
    team_row: pd.Series,
) -> pd.DataFrame:
    """
    Returns the full league-season dataframe for the selected team.
    """

    mask = (
        (df["source_league_slug"] == team_row["source_league_slug"])
        & (df["source_season"] == team_row["source_season"])
    )

    return df[mask].copy()


def _get_style_score_value(
    style_scores: pd.DataFrame,
    *,
    score_col: str,
) -> float | None:
    """
    Reads a style score value from the style score table.
    """

    style_label = TEAM_STYLE_SCORE_LABELS.get(score_col)

    if style_label is None:
        return None

    row = style_scores[style_scores["style_area"] == style_label]

    if row.empty:
        return None

    return row.iloc[0]["score"]


def _build_overview(
    team_row: pd.Series,
) -> pd.DataFrame:
    """
    Builds a compact opponent overview.
    """

    columns = [
        "contestant_name",
        "source_country_name",
        "source_league_name",
        "source_season",
        "Games Played",
        "Goals",
        "Goals Conceded",
        "Clean Sheets",
        "Possession Percentage",
        "PPDA",
    ]

    available_cols = [
        col for col in columns
        if col in team_row.index
    ]

    return pd.DataFrame([team_row[available_cols]]).reset_index(drop=True)


def _build_style_interpretation(
    style_scores: pd.DataFrame,
) -> pd.DataFrame:
    """
    Converts style scores into opposition report interpretation.
    """

    rows = []

    for score_col, rule in OPPOSITION_STYLE_RULES.items():
        score = _get_style_score_value(
            style_scores,
            score_col=score_col,
        )

        if score is None:
            continue

        band = _score_band(score)

        rows.append(
            {
                "area": rule["area"],
                "style_area": rule["label"],
                "score": score,
                "band": band,
                "interpretation": rule.get(band, ""),
                "preparation_focus": rule.get("prep_high", ""),
                "possible_vulnerability": rule.get("vulnerability_low", ""),
            }
        )

    return (
        pd.DataFrame(rows)
        .sort_values("score", ascending=False)
        .reset_index(drop=True)
    )


def _build_main_strengths(
    interpretation_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Builds main opponent strengths from high style scores.
    """

    strengths = interpretation_df[
        interpretation_df["band"] == "high"
    ].copy()

    if strengths.empty:
        strengths = (
            interpretation_df
            .sort_values("score", ascending=False)
            .head(3)
            .copy()
        )

    return strengths[
        [
            "style_area",
            "score",
            "interpretation",
        ]
    ].reset_index(drop=True)


def _build_possible_vulnerabilities(
    interpretation_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Builds possible opponent vulnerabilities from low style scores.
    """

    vulnerabilities = interpretation_df[
        interpretation_df["band"] == "low"
    ].copy()

    if vulnerabilities.empty:
        vulnerabilities = (
            interpretation_df
            .sort_values("score", ascending=True)
            .head(3)
            .copy()
        )

    return vulnerabilities[
        [
            "style_area",
            "score",
            "possible_vulnerability",
        ]
    ].reset_index(drop=True)


def _build_preparation_focus(
    interpretation_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Builds preparation focus points from high style scores.
    """

    high_traits = interpretation_df[
        interpretation_df["band"] == "high"
    ].copy()

    if high_traits.empty:
        high_traits = (
            interpretation_df
            .sort_values("score", ascending=False)
            .head(3)
            .copy()
        )

    rows = []

    for _, row in high_traits.iterrows():
        if not row["preparation_focus"]:
            continue

        rows.append(
            {
                "style_area": row["style_area"],
                "score": row["score"],
                "preparation_focus": row["preparation_focus"],
            }
        )

    if not rows:
        rows.append(
            {
                "style_area": "Overall",
                "score": pd.NA,
                "preparation_focus": (
                    "No extreme style profile stands out. Prepare for a balanced opponent and use video to refine match-specific details."
                ),
            }
        )

    return pd.DataFrame(rows)


def _flatten_metric_groups(
    metric_groups: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Combines grouped metric tables into one support table.
    """

    rows = []

    for group_key, group_df in metric_groups.items():
        if group_df.empty:
            continue

        temp = group_df.copy()
        temp["metric_group"] = group_key
        rows.append(temp)

    if not rows:
        return pd.DataFrame()

    return pd.concat(rows, ignore_index=True)


# =========================
# PUBLIC FUNCTION
# =========================

def build_opposition_report(
    df: pd.DataFrame,
    *,
    team_option_label: str,
) -> dict[str, Any]:
    """
    Builds a structured opposition report helper for one selected team.

    This is a data-led helper, not a full final written report.
    """

    if df.empty:
        raise ValueError("Cannot build opposition report from an empty dataframe.")

    team_row = select_team_row_by_option(
        df,
        team_option_label=team_option_label,
    )

    league_df = _get_league_season_df(
        df,
        team_row,
    )

    style_profile = build_team_style_profile(
        df,
        team_name=team_row["contestant_name"],
        league_name=team_row["source_league_name"],
        season=team_row["source_season"],
    )

    style_interpretation = _build_style_interpretation(
        style_profile["style_scores"],
    )

    attacking_profile = style_interpretation[
        style_interpretation["area"] == "attack"
    ].reset_index(drop=True)

    defensive_profile = style_interpretation[
        style_interpretation["area"] == "defence"
    ].reset_index(drop=True)

    metric_groups = build_team_metric_groups(
        team_row=team_row,
        df=league_df,
    )

    key_metrics = _flatten_metric_groups(
        metric_groups,
    )

    return {
        "overview": _build_overview(team_row),
        "attacking_profile": attacking_profile,
        "defensive_profile": defensive_profile,
        "main_strengths": _build_main_strengths(style_interpretation),
        "possible_vulnerabilities": _build_possible_vulnerabilities(style_interpretation),
        "preparation_focus": _build_preparation_focus(style_interpretation),
        "style_scores": style_profile["style_scores"],
        "key_metrics": key_metrics,
    }