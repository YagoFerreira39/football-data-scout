# =========================
# TEAM STYLE DOMAIN LOGIC
# =========================

import pandas as pd

from src.config.team_style import (
    TEAM_STYLE_PROFILE_CONFIG,
    TEAM_STYLE_SCORE_COLUMNS,
    TEAM_STYLE_SCORE_LABELS,
)


# =========================
# EXTRA STYLE METRICS
# =========================

def add_team_style_extra_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds extra derived metrics required by the team style model.

    These are row-level calculations, so they are safe to run on all teams.
    """

    df = df.copy()

    if "Games Played" not in df.columns:
        return df

    games = df["Games Played"].replace(0, pd.NA)

    per_game_columns = {
        "Successful Passes Opposition Half": "successful_passes_opp_half_per_game",
        "Successful Passes Own Half": "successful_passes_own_half_per_game",
        "Number of Defensive Actions": "defensive_actions_per_game",
        "Successful Launches": "successful_launches_per_game",
        "Unsuccessful Launches": "unsuccessful_launches_per_game",
        "Successful Long Passes": "successful_long_passes_per_game",
        "Unsuccessful Long Passes": "unsuccessful_long_passes_per_game",
        "Successful Crosses open play": "successful_crosses_open_play_per_game",
        "Unsuccessful Crosses open play": "unsuccessful_crosses_open_play_per_game",
    }

    for raw_col, new_col in per_game_columns.items():
        if raw_col in df.columns:
            df[new_col] = df[raw_col] / games

    # Long passes
    if {"Successful Long Passes", "Unsuccessful Long Passes"}.issubset(df.columns):
        total_long_passes = (
            df["Successful Long Passes"] + df["Unsuccessful Long Passes"]
        )

        df["long_passes_per_game"] = total_long_passes / games

        if "Total Passes" in df.columns:
            df["long_pass_share_pct"] = (
                total_long_passes / df["Total Passes"].replace(0, pd.NA) * 100
            )

    # Launches
    if {"Successful Launches", "Unsuccessful Launches"}.issubset(df.columns):
        total_launches = (
            df["Successful Launches"] + df["Unsuccessful Launches"]
        )

        df["launches_per_game"] = total_launches / games

    # Open-play crosses
    if {
        "Successful Crosses open play",
        "Unsuccessful Crosses open play",
    }.issubset(df.columns):
        total_crosses = (
            df["Successful Crosses open play"]
            + df["Unsuccessful Crosses open play"]
        )

        df["open_play_crosses_per_game"] = total_crosses / games
        df["open_play_cross_accuracy_pct"] = (
            df["Successful Crosses open play"]
            / total_crosses.replace(0, pd.NA)
            * 100
        )

        if "Total Passes" in df.columns:
            df["cross_share_pct"] = (
                total_crosses / df["Total Passes"].replace(0, pd.NA) * 100
            )

    return df


# =========================
# STYLE SCORE CALCULATION
# =========================

def percentile_score(series: pd.Series) -> pd.Series:
    """
    Converts values into percentile scores from 0 to 100.
    """

    return series.rank(pct=True) * 100


def build_team_style_scores(
    df: pd.DataFrame,
    *,
    group_cols: list[str] | None = None,
    config: dict = TEAM_STYLE_PROFILE_CONFIG,
) -> pd.DataFrame:
    """
    Adds team style score columns.

    Scores are calculated inside each league-season group.
    """

    df = df.copy()

    if group_cols is None:
        group_cols = ["source_league_slug", "source_season"]

    score_cols = []

    for style_key, style_data in config.items():
        score_col = f"{style_key}_score"
        score_cols.append(score_col)

        metric_scores = []

        # Higher value means stronger trait
        for col in style_data["higher_is_better"]:
            if col not in df.columns:
                continue

            metric_score = (
                df.groupby(group_cols)[col]
                .transform(percentile_score)
            )

            metric_scores.append(metric_score)

        # Lower value means stronger trait
        for col in style_data["lower_is_better"]:
            if col not in df.columns:
                continue

            metric_score = (
                100
                - df.groupby(group_cols)[col]
                .transform(percentile_score)
            )

            metric_scores.append(metric_score)

        if metric_scores:
            df[score_col] = pd.concat(metric_scores, axis=1).mean(axis=1)
        else:
            df[score_col] = pd.NA

    available_score_cols = [
        col for col in score_cols
        if col in df.columns
    ]

    if available_score_cols:
        df["overall_style_intensity_score"] = df[available_score_cols].mean(axis=1)
    else:
        df["overall_style_intensity_score"] = pd.NA

    return df


def prepare_team_style_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares the dataframe for team style usage.
    """

    df = add_team_style_extra_metrics(df)

    df = build_team_style_scores(
        df,
        group_cols=["source_league_slug", "source_season"],
    )

    return df


# =========================
# TEAM STYLE PROFILE
# =========================

def build_team_style_profile(
    df: pd.DataFrame,
    *,
    team_name: str,
    league_name: str,
    season: str,
) -> dict[str, pd.DataFrame]:
    """
    Builds style tables for one selected team.
    """

    team_mask = (
        (df["contestant_name"] == team_name)
        & (df["source_league_name"] == league_name)
        & (df["source_season"] == season)
    )

    team_df = df[team_mask]

    if team_df.empty:
        raise ValueError("Selected team was not found in team style dataframe.")

    team_row = team_df.iloc[0]

    league_mask = (
        (df["source_league_slug"] == team_row["source_league_slug"])
        & (df["source_season"] == team_row["source_season"])
    )

    league_df = df[league_mask].copy()

    teams_count = league_df["contestant_name"].nunique()

    rows = []

    for score_col in TEAM_STYLE_SCORE_COLUMNS:
        if score_col not in df.columns:
            continue

        score = team_row[score_col]

        rank = (
            league_df[score_col]
            .rank(ascending=False, method="min")
            .loc[team_row.name]
        )

        rows.append(
            {
                "style_area": TEAM_STYLE_SCORE_LABELS.get(score_col, score_col),
                "score": score,
                "league_rank": int(rank) if pd.notna(rank) else pd.NA,
                "league_teams": teams_count,
            }
        )

    style_scores = (
        pd.DataFrame(rows)
        .sort_values("score", ascending=False)
        .reset_index(drop=True)
    )

    strongest_traits = style_scores.head(3).reset_index(drop=True)

    weakest_traits = (
        style_scores
        .sort_values("score", ascending=True)
        .head(3)
        .reset_index(drop=True)
    )

    return {
        "style_scores": style_scores,
        "strongest_traits": strongest_traits,
        "weakest_traits": weakest_traits,
    }