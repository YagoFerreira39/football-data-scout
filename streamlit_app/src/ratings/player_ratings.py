from __future__ import annotations

import numpy as np
import pandas as pd


RATING_FIXED_COLUMNS = [
    "player",
    "team_within_selected_timeframe",
    "main_position",
    "age",
    "minutes_played",
]

def build_player_ratings_table(
    df: pd.DataFrame,
    league_name: str,
    season: str,
    positions: list[str],
    category_weights: dict[str, float],
    feature_weights: dict[str, dict[str, float]],
    minimum_minutes_played: int = 1000,
) -> pd.DataFrame:
    filtered_df = df.copy()

    filtered_df = filtered_df[
        filtered_df["league_name"].astype(str).eq(str(league_name))
        & filtered_df["season"].astype(str).eq(str(season))
    ].copy()

    filtered_df = filtered_df[
        filtered_df["main_position"].isin(positions)
    ].copy()

    filtered_df = filtered_df[
        filtered_df["minutes_played"] >= minimum_minutes_played
    ].copy()

    if filtered_df.empty:
        return pd.DataFrame()

    metric_columns = get_rating_metric_columns(filtered_df)

    normalized_df = normalize_metric_columns(
        df=filtered_df,
        metric_columns=metric_columns,
    )

    role_df = create_role_rating_columns(
        df=normalized_df,
        feature_weights=feature_weights,
    )

    ratings_df = create_ratings_df(role_df)

    ratings_df = normalize_attribute_columns(ratings_df)

    ratings_df = create_overall_rating(
        ratings_df=ratings_df,
        category_weights=category_weights,
    )

    ratings_df = prepare_ratings_table(ratings_df)

    return ratings_df

def normalize_series(series: pd.Series) -> pd.Series:
    min_value = series.min()
    max_value = series.max()

    if pd.isna(min_value) or pd.isna(max_value) or max_value == min_value:
        return pd.Series(0.0, index=series.index)

    return (series - min_value) / (max_value - min_value)


def get_rating_metric_columns(
    df: pd.DataFrame,
    fixed_columns: list[str] | None = None,
) -> list[str]:
    fixed_columns = fixed_columns or RATING_FIXED_COLUMNS

    excluded_columns = set(
        fixed_columns
        + [
            "team",
            "position",
            "positions",
            "birth_country",
            "passport_country",
            "foot",
            "height",
            "weight",
            "market_value",
            "contract_expires",
            "on_loan",
            "league",
            "league_base",
            "league_name",
            "league_country",
            "season",
        ]
    )

    metric_columns = []

    for column in df.columns:
        if column in excluded_columns:
            continue

        if pd.api.types.is_numeric_dtype(df[column]):
            metric_columns.append(column)

    return metric_columns


def normalize_metric_columns(
    df: pd.DataFrame,
    metric_columns: list[str],
) -> pd.DataFrame:
    normalized_df = df.copy()

    for column in metric_columns:
        normalized_df[column] = pd.to_numeric(
            normalized_df[column],
            errors="coerce",
        )

        normalized_df[column] = normalized_df[column].fillna(
            normalized_df[column].median()
        )

        normalized_df[column] = normalize_series(normalized_df[column])

    return normalized_df


def create_role_rating_columns(
    df: pd.DataFrame,
    feature_weights: dict[str, dict[str, float]],
) -> pd.DataFrame:
    ratings_df = df.copy()
    new_columns = {}

    for category, metrics in feature_weights.items():
        category_score = 0.0

        for metric, weight in metrics.items():
            if metric not in ratings_df.columns:
                raise KeyError(
                    f"Metric '{metric}' was not found in the dataframe. "
                    f"Check the rating profile config."
                )

            metric_rating_column = f"{metric}_rating"
            new_columns[metric_rating_column] = ratings_df[metric] * weight
            category_score += new_columns[metric_rating_column]

        category_column = f"{category}_att"
        new_columns[category_column] = category_score

    return pd.concat(
        [ratings_df, pd.DataFrame(new_columns, index=ratings_df.index)],
        axis=1,
    )


def create_ratings_df(
    df: pd.DataFrame,
    fixed_columns: list[str] | None = None,
) -> pd.DataFrame:
    fixed_columns = fixed_columns or RATING_FIXED_COLUMNS
    available_fixed_columns = [
        column for column in fixed_columns
        if column in df.columns
    ]

    att_columns = [
        column for column in df.columns
        if column.endswith("_att")
    ]

    return df[available_fixed_columns + att_columns].copy()


def normalize_attribute_columns(ratings_df: pd.DataFrame) -> pd.DataFrame:
    df = ratings_df.copy()

    att_columns = [
        column for column in df.columns
        if column.endswith("_att")
    ]

    for column in att_columns:
        df[column] = normalize_series(df[column])

    return df


def create_overall_rating(
    ratings_df: pd.DataFrame,
    category_weights: dict[str, float],
) -> pd.DataFrame:
    df = ratings_df.copy()

    overall_rating = 0.0

    for category, weight in category_weights.items():
        category_column = f"{category}_att"

        if category_column not in df.columns:
            raise KeyError(
                f"Category column '{category_column}' was not found. "
                f"Check category_weights and feature_weights names."
            )

        overall_rating += df[category_column] * weight

    df["overall_rating"] = normalize_series(overall_rating)

    return df


def prepare_ratings_table(ratings_df: pd.DataFrame) -> pd.DataFrame:
    df = ratings_df.copy()

    rating_columns = [
        column for column in df.columns
        if column.endswith("_att") or column == "overall_rating"
    ]

    df[rating_columns] = df[rating_columns] * 100
    df[rating_columns] = df[rating_columns].round(2)

    df = df.sort_values(
        by="overall_rating",
        ascending=False,
    ).reset_index(drop=True)

    df.insert(0, "rank", range(1, len(df) + 1))

    return df