# =========================
# PLAY STYLE PROFILE DOMAIN LOGIC
# =========================

import pandas as pd

from src.config.play_style_profile import (
    PLAY_STYLE_DIMENSIONS,
    PLAY_STYLE_SCORE_PREFIX,
)
from src.domain.team_profile import select_team_row_by_option


# =========================
# HELPERS
# =========================

def percentile_score(series: pd.Series) -> pd.Series:
    """
    Converts a metric into a 0-100 percentile score.
    """

    return series.rank(pct=True) * 100


def get_play_style_score_column(dimension_key: str) -> str:
    """
    Returns the dataframe column name for one play style dimension.
    """

    return f"{PLAY_STYLE_SCORE_PREFIX}_{dimension_key}_score"


def get_available_indicator_columns(
    df: pd.DataFrame,
    indicators: list[dict],
) -> list[str]:
    """
    Returns indicator columns available in the dataframe.
    """

    return [
        indicator["column"]
        for indicator in indicators
        if indicator["column"] in df.columns
    ]


def _build_weighted_component(
    df: pd.DataFrame,
    *,
    indicator: dict,
    group_cols: list[str],
    direction: str,
) -> pd.Series | None:
    """
    Builds one weighted percentile component.

    direction:
    - right: higher value pushes toward the right label
    - left: higher value pushes toward the left label
    """

    column = indicator["column"]
    weight = indicator["weight"]

    if column not in df.columns:
        return None

    score = (
        df.groupby(group_cols)[column]
        .transform(percentile_score)
    )

    if direction == "left":
        score = 100 - score

    return score * weight


def _build_dimension_score(
    df: pd.DataFrame,
    *,
    dimension_config: dict,
    group_cols: list[str],
) -> tuple[pd.Series, float, list[str]]:
    """
    Calculates one bipolar play-style dimension.

    Returns:
    - weighted score
    - available weight
    - used metric columns
    """

    components = []
    available_weight = 0.0
    used_metrics = []

    for indicator in dimension_config["right_indicators"]:
        component = _build_weighted_component(
            df,
            indicator=indicator,
            group_cols=group_cols,
            direction="right",
        )

        if component is None:
            continue

        components.append(component)
        available_weight += indicator["weight"]
        used_metrics.append(indicator["column"])

    for indicator in dimension_config["left_indicators"]:
        component = _build_weighted_component(
            df,
            indicator=indicator,
            group_cols=group_cols,
            direction="left",
        )

        if component is None:
            continue

        components.append(component)
        available_weight += indicator["weight"]
        used_metrics.append(indicator["column"])

    if not components or available_weight == 0:
        empty_score = pd.Series(pd.NA, index=df.index)
        return empty_score, available_weight, used_metrics

    score = sum(components) / available_weight

    return score, available_weight, used_metrics


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


# =========================
# PUBLIC CALCULATION FUNCTIONS
# =========================

def add_play_style_profile_scores(
    df: pd.DataFrame,
    *,
    group_cols: list[str] | None = None,
) -> pd.DataFrame:
    """
    Adds bipolar play-style scores to the dataframe.

    Scores are calculated inside each league-season.
    0 means closer to the left label.
    100 means closer to the right label.
    """

    df = df.copy()

    if group_cols is None:
        group_cols = ["source_league_slug", "source_season"]

    for dimension_key, dimension_config in PLAY_STYLE_DIMENSIONS.items():
        score_col = get_play_style_score_column(dimension_key)
        weight_col = f"{score_col}_available_weight"
        metrics_col = f"{score_col}_used_metrics"

        score, available_weight, used_metrics = _build_dimension_score(
            df,
            dimension_config=dimension_config,
            group_cols=group_cols,
        )

        df[score_col] = score
        df[weight_col] = available_weight
        df[metrics_col] = ", ".join(used_metrics)

    return df


def build_team_play_style_profile(
    df: pd.DataFrame,
    *,
    team_option_label: str,
) -> pd.DataFrame:
    """
    Builds chart-ready play-style profile data for one selected team.

    Output columns:
    - dimension_key
    - category
    - left_label
    - right_label
    - team_score
    - league_average
    - league_rank
    - league_teams
    - difference_from_league_average
    """

    if df.empty:
        raise ValueError("Cannot build play-style profile from an empty dataframe.")

    team_row = select_team_row_by_option(
        df,
        team_option_label=team_option_label,
    )

    league_df = _get_league_season_df(
        df,
        team_row,
    )

    teams_count = league_df["contestant_name"].nunique()

    rows = []

    for dimension_key, dimension_config in PLAY_STYLE_DIMENSIONS.items():
        score_col = get_play_style_score_column(dimension_key)
        weight_col = f"{score_col}_available_weight"
        metrics_col = f"{score_col}_used_metrics"

        if score_col not in df.columns:
            continue

        team_score = team_row[score_col]
        league_average = league_df[score_col].mean()

        rank = (
            league_df[score_col]
            .rank(ascending=False, method="min")
            .loc[team_row.name]
        )

        rows.append(
            {
                "dimension_key": dimension_key,
                "category": dimension_config["label"],
                "left_label": dimension_config["left_label"],
                "right_label": dimension_config["right_label"],
                "team_name": team_row["contestant_name"],
                "league_name": team_row["source_league_name"],
                "season": team_row["source_season"],
                "team_score": team_score,
                "league_average": league_average,
                "difference_from_league_average": team_score - league_average,
                "league_rank": int(rank) if pd.notna(rank) else pd.NA,
                "league_teams": teams_count,
                "available_weight": team_row.get(weight_col, pd.NA),
                "used_metrics": team_row.get(metrics_col, ""),
                "badge_sm": team_row.get("badge_sm", pd.NA),
                "badge_lg": team_row.get("badge_lg", pd.NA),
            }
        )

    return pd.DataFrame(rows)

def build_league_play_style_distribution(
    df: pd.DataFrame,
    *,
    team_option_label: str,
) -> pd.DataFrame:
    """
    Builds league distribution data for the selected team's league-season.

    Output has one row per team per play-style dimension.
    This is used for faded league dots in the visual.
    """

    if df.empty:
        raise ValueError("Cannot build play-style distribution from an empty dataframe.")

    team_row = select_team_row_by_option(
        df,
        team_option_label=team_option_label,
    )

    league_df = _get_league_season_df(
        df,
        team_row,
    )

    rows = []

    for dimension_key, dimension_config in PLAY_STYLE_DIMENSIONS.items():
        score_col = get_play_style_score_column(dimension_key)

        if score_col not in league_df.columns:
            continue

        for _, row in league_df.iterrows():
            rows.append(
                {
                    "dimension_key": dimension_key,
                    "category": dimension_config["label"],
                    "team_name": row["contestant_name"],
                    "score": row[score_col],
                    "is_selected_team": (
                        row["contestant_name"] == team_row["contestant_name"]
                    ),
                }
            )

    return pd.DataFrame(rows)
