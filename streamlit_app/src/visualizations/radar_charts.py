from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mplsoccer import Radar
from matplotlib.lines import Line2D

from src.config.chart_colors import BRAND_COLORS, CHART_COLORS
from src.config.feature_labels import FEATURE_LABELS
from src.visualizations.pizza_charts import (
    COMPARISON_GROUPS,
    get_all_features_for_position,
    get_comparison_group_for_position,
)

# SINGLE PLAYER RADAR
def plot_player_raw_radar_chart(
    df: pd.DataFrame,
    player_name: str,
    minimum_minutes_played: int,
    profile: str | None = None,
    mode: str = "position",
    player_column: str = "player",
    position_column: str = "main_position",
    minutes_column: str = "minutes_played",
):
    """
    Plot a raw-value radar chart for one player.

    The radar range for each metric is based on the min/max values
    from the selected comparison pool.

    It also plots the league-position mean for each feature.
    """
    if isinstance(df, pd.Series):
        raise TypeError(
            "plot_player_raw_radar_chart expected a pd.DataFrame, "
            "but received a pd.Series."
        )

    player_df = df[df[player_column].eq(player_name)].copy()

    if player_df.empty:
        raise ValueError(f"{player_name} not found in dataframe.")

    player_row = player_df.iloc[0]

    position = str(player_row[position_column])
    team = str(player_row.get("team", ""))
    season = str(player_row.get("season", ""))

    features = get_all_features_for_position(
        position=position,
        profile=profile,
    )

    comparison_df = _prepare_radar_comparison_df(
        df=df,
        features=features,
        position=position,
        mode=mode,
        position_column=position_column,
        minutes_column=minutes_column,
        minimum_minutes_played=minimum_minutes_played,
    )

    min_values, max_values = _build_raw_radar_ranges(
        comparison_df=comparison_df,
        features=features,
    )

    player_values = [
        _format_player_value(player_row.get(feature))
        for feature in features
    ]

    league_mean_values = []

    for feature in features:
        feature_mean = pd.to_numeric(
            comparison_df[feature],
            errors="coerce",
        ).mean()

        league_mean_values.append(
            _format_player_value(feature_mean)
        )

    labels = [
        _get_feature_label(feature)
        for feature in features
    ]

    radar = Radar(
        params=labels,
        min_range=min_values,
        max_range=max_values,
        round_int=[False] * len(labels),
        num_rings=4,
        ring_width=1,
        center_circle_radius=1,
    )

    fig, ax = radar.setup_axis(figsize=(8.5, 8.5))

    fig.patch.set_facecolor(BRAND_COLORS["background_main"])
    ax.set_facecolor(BRAND_COLORS["background_main"])

    radar.draw_circles(
        ax=ax,
        facecolor=BRAND_COLORS["background_panel"],
        edgecolor=BRAND_COLORS["border"],
        lw=1,
        alpha=0.9,
    )

    radar.draw_radar_compare(
        values=player_values,
        compare_values=league_mean_values,
        ax=ax,
        kwargs_radar=dict(
            facecolor="#FACC15",
            alpha=0.30,
            edgecolor="#FACC15",
            linewidth=2.3,
        ),
        kwargs_compare=dict(
            facecolor="#F43F5E",
            alpha=0.35,
            edgecolor="#F43F5E",
            linewidth=2.0,
            linestyle="--",
        ),
    )

    radar.draw_range_labels(
        ax=ax,
        fontsize=8,
        color=BRAND_COLORS["text_body"],
    )

    radar.draw_param_labels(
        ax=ax,
        fontsize=8,
        color=BRAND_COLORS["text_main"],
    )

    comparison_group = get_comparison_group_for_position(position)
    footer_mode = "vs Position" if mode == "position" else "vs All Players"

    fig.text(
        0.5,
        0.965,
        f"{player_name}",
        ha="center",
        color=BRAND_COLORS["text_main"],
        fontsize=16,
        fontweight="bold",
    )

    legend_handles = [
        Line2D(
            [0],
            [0],
            color="#FACC15",
            lw=3,
            label=player_name,
        ),
        Line2D(
            [0],
            [0],
            color="#F43F5E",
            lw=3,
            linestyle="--",
            label=f"{comparison_group} Mean",
        ),
    ]

    fig.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.92),
        ncol=2,
        frameon=False,
        fontsize=10,
        labelcolor=BRAND_COLORS["text_main"],
    )

    fig.text(
        0.5,
        0.035,
        (
            f"Raw values scaled by league min/max ({footer_mode}) | "
            f"{comparison_df.shape[0]} {comparison_group} players | "
            f"{minimum_minutes_played}+ minutes | {season}"
        ),
        ha="center",
        color=BRAND_COLORS["text_muted"],
        fontsize=10,
    )

    metadata = {
        "player": player_name,
        "team": team,
        "season": season,
        "position": position,
        "profile": profile,
        "comparison_group": comparison_group,
        "total_players_comparison": comparison_df.shape[0],
        "minimum_minutes_played": minimum_minutes_played,
        "mode": mode,
    }

    return fig, metadata

# Two-Player Radar Comparison
def plot_players_raw_radar_comparison(
    df: pd.DataFrame,
    player_name_1: str,
    player_name_2: str,
    minimum_minutes_played: int,
    profile: str | None = None,
    mode: str = "position",
    player_column: str = "player",
    position_column: str = "main_position",
    minutes_column: str = "minutes_played",
):
    """
    Plot a raw-value 1v1 radar chart.

    Both players are plotted using the same features and the same
    league-position min/max ranges.
    """
    if isinstance(df, pd.Series):
        raise TypeError(
            "plot_players_raw_radar_comparison expected a pd.DataFrame, "
            "but received a pd.Series."
        )

    player_1_df = df[df[player_column].eq(player_name_1)].copy()
    player_2_df = df[df[player_column].eq(player_name_2)].copy()

    if player_1_df.empty:
        raise ValueError(f"{player_name_1} not found in dataframe.")

    if player_2_df.empty:
        raise ValueError(f"{player_name_2} not found in dataframe.")

    player_1 = player_1_df.iloc[0]
    player_2 = player_2_df.iloc[0]

    position_1 = str(player_1[position_column])
    position_2 = str(player_2[position_column])

    comparison_group_1 = get_comparison_group_for_position(position_1)
    comparison_group_2 = get_comparison_group_for_position(position_2)

    if comparison_group_1 != comparison_group_2:
        raise ValueError(
            "Both players should belong to the same comparison group "
            "for a meaningful 1v1 radar."
        )

    features = get_all_features_for_position(
        position=position_1,
        profile=profile,
    )

    comparison_df = _prepare_radar_comparison_df(
        df=df,
        features=features,
        position=position_1,
        mode=mode,
        position_column=position_column,
        minutes_column=minutes_column,
        minimum_minutes_played=minimum_minutes_played,
    )

    min_values, max_values = _build_raw_radar_ranges(
        comparison_df=comparison_df,
        features=features,
    )

    player_1_values = [
        _format_player_value(player_1.get(feature))
        for feature in features
    ]

    player_2_values = [
        _format_player_value(player_2.get(feature))
        for feature in features
    ]

    labels = [
        _get_feature_label(feature)
        for feature in features
    ]

    radar = Radar(
        params=labels,
        min_range=min_values,
        max_range=max_values,
        round_int=[False] * len(labels),
        num_rings=4,
        ring_width=1,
        center_circle_radius=1,
    )

    fig, ax = radar.setup_axis(figsize=(8.5, 8.5))

    fig.patch.set_facecolor(BRAND_COLORS["background_main"])
    ax.set_facecolor(BRAND_COLORS["background_main"])

    radar.draw_circles(
        ax=ax,
        facecolor=BRAND_COLORS["background_panel"],
        edgecolor=BRAND_COLORS["border"],
        lw=1,
        alpha=0.9,
    )

    radar.draw_radar_compare(
        values=player_1_values,
        compare_values=player_2_values,
        ax=ax,
        kwargs_radar=dict(
            facecolor=CHART_COLORS["cyan"],
            alpha=0.32,
            edgecolor=CHART_COLORS["cyan"],
            linewidth=2.2,
        ),
        kwargs_compare=dict(
            facecolor=CHART_COLORS["magenta"],
            alpha=0.30,
            edgecolor=CHART_COLORS["magenta"],
            linewidth=2.2,
        ),
    )

    radar.draw_range_labels(
        ax=ax,
        fontsize=8,
        color=BRAND_COLORS["text_body"],
    )

    radar.draw_param_labels(
        ax=ax,
        fontsize=8,
        color=BRAND_COLORS["text_main"],
    )

    fig.text(
        0.5,
        0.965,
        f"{player_name_1} vs {player_name_2} | Raw Value Radar",
        ha="center",
        color=BRAND_COLORS["text_main"],
        fontsize=16,
        fontweight="bold",
    )

    legend_handles = [
        Line2D(
            [0],
            [0],
            color=CHART_COLORS["cyan"],
            lw=3,
            label=player_name_1,
        ),
        Line2D(
            [0],
            [0],
            color=CHART_COLORS["magenta"],
            lw=3,
            label=player_name_2,
        ),
    ]

    fig.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.92),
        ncol=2,
        frameon=False,
        fontsize=10,
        labelcolor=BRAND_COLORS["text_main"],
    )

    footer_mode = "vs Position" if mode == "position" else "vs All Players"

    fig.text(
        0.5,
        0.035,
        (
            f"Raw values scaled by league min/max ({footer_mode}) | "
            f"{comparison_df.shape[0]} {comparison_group_1} players | "
            f"{minimum_minutes_played}+ minutes"
        ),
        ha="center",
        color=BRAND_COLORS["text_muted"],
        fontsize=10,
    )

    metadata = {
        "player_1": player_name_1,
        "player_2": player_name_2,
        "position_1": position_1,
        "position_2": position_2,
        "profile": profile,
        "comparison_group": comparison_group_1,
        "total_players_comparison": comparison_df.shape[0],
        "minimum_minutes_played": minimum_minutes_played,
        "mode": mode,
    }

    return fig, metadata

# HELPERS
def _get_feature_label(feature: str) -> str:
    return FEATURE_LABELS.get(feature, feature)


def _format_player_value(value) -> float:
    if value is None or pd.isna(value):
        return 0.0

    return float(value)


def _prepare_radar_comparison_df(
    df: pd.DataFrame,
    features: list[str],
    position: str,
    mode: str = "position",
    position_column: str = "main_position",
    minutes_column: str = "minutes_played",
    minimum_minutes_played: int = 900,
) -> pd.DataFrame:
    plot_df = df.copy()

    plot_df = plot_df[
        plot_df[minutes_column] >= minimum_minutes_played
    ].copy()

    if mode == "position":
        comparison_group = get_comparison_group_for_position(position)
        valid_positions = COMPARISON_GROUPS.get(comparison_group, [position])

        plot_df = plot_df[
            plot_df[position_column].isin(valid_positions)
        ].copy()

    for feature in features:
        plot_df[feature] = pd.to_numeric(plot_df[feature], errors="coerce")

    plot_df = plot_df.dropna(subset=features, how="all")

    return plot_df.reset_index(drop=True)


def _build_raw_radar_ranges(
    comparison_df: pd.DataFrame,
    features: list[str],
) -> tuple[list[float], list[float]]:
    min_values = []
    max_values = []

    for feature in features:
        feature_values = pd.to_numeric(
            comparison_df[feature],
            errors="coerce",
        ).dropna()

        if feature_values.empty:
            min_value = 0.0
            max_value = 1.0
        else:
            min_value = float(feature_values.min())
            max_value = float(feature_values.max())

            if min_value == max_value:
                padding = abs(max_value) * 0.10 if max_value != 0 else 1.0
                min_value = min_value - padding
                max_value = max_value + padding

        min_values.append(min_value)
        max_values.append(max_value)

    return min_values, max_values