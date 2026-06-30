# =========================
# TEAM PROFILE DOMAIN LOGIC
# =========================

import pandas as pd

from src.config.team_profile import (
    LOWER_IS_BETTER_TEAM_METRICS,
    TEAM_PROFILE_ID_COLUMNS,
    TEAM_PROFILE_METRIC_GROUPS,
    TEAM_PROFILE_OVERVIEW_COLUMNS,
)


def format_metric_name(column: str) -> str:
    """
    Converts a dataframe column into a readable metric label.
    """

    return (
        column.replace("_", " ")
        .replace("pct", "%")
        .replace("PPDA", "PPDA")
        .title()
    )


def get_available_team_options(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns unique team options from the currently filtered dataframe.
    """

    cols = [
        "contestant_name",
        "source_country_name",
        "source_league_name",
        "source_season",
        "source_league_slug",
    ]

    available_cols = [col for col in cols if col in df.columns]

    teams_df = (
        df[available_cols]
        .drop_duplicates()
        .sort_values(["contestant_name", "source_league_name", "source_season"])
        .reset_index(drop=True)
    )

    teams_df["team_option_label"] = (
        teams_df["contestant_name"]
        + " | "
        + teams_df["source_league_name"]
        + " | "
        + teams_df["source_season"]
    )

    return teams_df


def select_team_row_by_option(
    df: pd.DataFrame,
    *,
    team_option_label: str,
) -> pd.Series:
    """
    Selects one team row using the option label created by get_available_team_options().
    """

    teams_df = get_available_team_options(df)

    selected = teams_df[
        teams_df["team_option_label"] == team_option_label
    ]

    if selected.empty:
        raise ValueError("Selected team was not found.")

    selected_team = selected.iloc[0]

    mask = (
        (df["contestant_name"] == selected_team["contestant_name"])
        & (df["source_league_name"] == selected_team["source_league_name"])
        & (df["source_season"] == selected_team["source_season"])
    )

    if "source_league_slug" in df.columns:
        mask = mask & (
            df["source_league_slug"] == selected_team["source_league_slug"]
        )

    team_rows = df[mask]

    if team_rows.empty:
        raise ValueError("Selected team row was not found in dataframe.")

    return team_rows.iloc[0]


def build_team_overview(
    team_row: pd.Series,
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Builds a compact overview table for one team.
    """

    columns = TEAM_PROFILE_ID_COLUMNS + TEAM_PROFILE_OVERVIEW_COLUMNS
    available_cols = [col for col in columns if col in df.columns]

    return pd.DataFrame([team_row[available_cols]]).reset_index(drop=True)


def get_metric_rank(
    df: pd.DataFrame,
    *,
    metric: str,
    row_index,
) -> int:
    """
    Calculates the rank of one metric inside the selected dataframe.
    """

    if metric not in df.columns:
        return pd.NA

    ascending = metric in LOWER_IS_BETTER_TEAM_METRICS

    ranks = df[metric].rank(
        ascending=ascending,
        method="min",
    )

    value = ranks.loc[row_index]

    if pd.isna(value):
        return pd.NA

    return int(value)


def build_team_metric_groups(
    team_row: pd.Series,
    df: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """
    Builds metric tables grouped by football area.
    """

    metric_groups = {}

    teams_count = (
        df["contestant_name"].nunique()
        if "contestant_name" in df.columns
        else len(df)
    )

    for group_key, group_data in TEAM_PROFILE_METRIC_GROUPS.items():
        rows = []

        for metric in group_data["columns"]:
            if metric not in df.columns:
                continue

            value = team_row[metric]

            rank = get_metric_rank(
                df,
                metric=metric,
                row_index=team_row.name,
            )

            rows.append(
                {
                    "metric": format_metric_name(metric),
                    "column": metric,
                    "value": value,
                    "rank_in_selected_group": rank,
                    "teams_count": teams_count,
                }
            )

        metric_groups[group_key] = pd.DataFrame(rows)

    return metric_groups


def build_team_profile(
    df: pd.DataFrame,
    *,
    team_option_label: str,
) -> dict[str, pd.DataFrame]:
    """
    Builds the full team profile object for the selected team.
    """

    if df.empty:
        raise ValueError("Cannot build team profile from an empty dataframe.")

    team_row = select_team_row_by_option(
        df,
        team_option_label=team_option_label,
    )

    overview = build_team_overview(
        team_row=team_row,
        df=df,
    )

    metric_groups = build_team_metric_groups(
        team_row=team_row,
        df=df,
    )

    return {
        "overview": overview,
        "metric_groups": metric_groups,
    }