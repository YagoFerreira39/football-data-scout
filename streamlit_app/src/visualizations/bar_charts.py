from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.config.chart_colors import BRAND_COLORS, GROUP_COLORS
from src.config.feature_labels import FEATURE_LABELS
from src.visualizations.pizza_charts import (
    compute_percentiles,
    get_all_features_for_position,
    get_comparison_group_for_position,
    get_feature_groups_for_position,
    get_role_for_position,
    COMPARISON_GROUPS,
)


def _get_feature_label(feature: str) -> str:
    return FEATURE_LABELS.get(feature, feature)


def _get_feature_group_map(position: str, profile: str | None = None) -> dict[str, str]:
    """
    Returns:
        {
            "shots_per_90": "Goal Threat",
            "xg_per_90": "Goal Threat",
            ...
        }
    """
    feature_groups = get_feature_groups_for_position(
        position=position,
        profile=profile,
    )

    feature_to_group = {}

    for group_name, features in feature_groups.items():
        for feature in features:
            feature_to_group[feature] = group_name

    return feature_to_group


def _get_bar_colors(
    features: list[str],
    position: str,
    profile: str | None = None,
) -> list[str]:
    feature_to_group = _get_feature_group_map(
        position=position,
        profile=profile,
    )

    colors = []

    for feature in features:
        group_name = feature_to_group.get(feature)
        colors.append(GROUP_COLORS.get(group_name, "#94A3B8"))

    return colors

def build_player_percentile_profile(
    df: pd.DataFrame,
    player_name: str,
    minimum_minutes_played: int,
    profile: str | None = None,
    mode: str = "position",
    player_column: str = "player",
    position_column: str = "main_position",
    minutes_column: str = "minutes_played",
) -> tuple[pd.DataFrame, dict]:
    """
    Build percentile data for one player using the same logic as the pizza chart.

    Returns:
        profile_df:
            DataFrame with feature, label, percentile, group and color.

        metadata:
            Extra information for title/footer.
    """
    plot_df = df.copy()

    if isinstance(plot_df, pd.Series):
        raise TypeError(
            "build_player_percentile_profile expected a pd.DataFrame, "
            "but received a pd.Series."
        )

    plot_df = plot_df[
        plot_df[minutes_column] >= minimum_minutes_played
    ].copy()

    player_df = plot_df[
        plot_df[player_column].eq(player_name)
    ].copy()

    if player_df.empty:
        raise ValueError(f"{player_name} not found in comparison dataframe.")

    player_row = player_df.iloc[0]

    position = str(player_row[position_column])
    team = str(player_row.get("team", ""))
    season = str(player_row.get("season", ""))

    features = get_all_features_for_position(
        position=position,
        profile=profile,
    )

    comparison_group = get_comparison_group_for_position(position)
    valid_positions = COMPARISON_GROUPS.get(comparison_group, [position])

    if mode == "position":
        df_pct = compute_percentiles(
            plot_df,
            features,
            position=position,
        )

        total_players_comparison = plot_df[
            plot_df[position_column].isin(valid_positions)
        ].shape[0]
    else:
        df_pct = compute_percentiles(
            plot_df,
            features,
        )

        total_players_comparison = plot_df.shape[0]

    player_pct_row = df_pct[
        df_pct[player_column].eq(player_name)
    ]

    if player_pct_row.empty:
        raise ValueError(
            f"{player_name} was removed from the percentile dataframe."
        )

    values = player_pct_row[features].values.flatten()
    values = np.nan_to_num(values, nan=0).round(1)

    feature_to_group = _get_feature_group_map(
        position=position,
        profile=profile,
    )

    colors = _get_bar_colors(
        features=features,
        position=position,
        profile=profile,
    )

    profile_df = pd.DataFrame(
        {
            "feature": features,
            "label": [_get_feature_label(feature) for feature in features],
            "percentile": values,
            "group": [feature_to_group.get(feature, "Other") for feature in features],
            "color": colors,
        }
    )

    metadata = {
        "player": player_name,
        "team": team,
        "season": season,
        "position": position,
        "profile": profile,
        "comparison_group": comparison_group,
        "total_players_comparison": total_players_comparison,
        "minimum_minutes_played": minimum_minutes_played,
        "mode": mode,
    }

    return profile_df, metadata

def plot_player_percentile_bar_chart(
    df: pd.DataFrame,
    player_name: str,
    minimum_minutes_played: int,
    profile: str | None = None,
    mode: str = "position",
    sort_values: bool = True,
):
    """
    Plot a horizontal bar chart showing percentile ranks for one player.

    This uses the same percentile logic and feature groups as the pizza chart.
    """
    profile_df, metadata = build_player_percentile_profile(
        df=df,
        player_name=player_name,
        minimum_minutes_played=minimum_minutes_played,
        profile=profile,
        mode=mode,
    )

    if sort_values:
        profile_df = profile_df.sort_values(
            "percentile",
            ascending=True,
        )

    fig_height = max(5.0, len(profile_df) * 0.38)

    fig, ax = plt.subplots(
        figsize=(8.5, fig_height),
        dpi=150,
    )

    fig.patch.set_facecolor(BRAND_COLORS["background_main"])
    ax.set_facecolor(BRAND_COLORS["background_main"])

    bars = ax.barh(
        profile_df["label"],
        profile_df["percentile"],
        color=profile_df["color"],
        alpha=0.92,
        height=0.64,
    )

    ax.set_xlim(0, 100)

    ax.set_xlabel(
        "Percentile Rank",
        color=BRAND_COLORS["text_main"],
        fontsize=11,
        labelpad=10,
    )

    ax.set_title(
        f"{metadata['player']} | Percentile Profile",
        color=BRAND_COLORS["text_main"],
        fontsize=15,
        weight="bold",
        pad=14,
    )

    ax.grid(
        axis="x",
        color=BRAND_COLORS["border"],
        alpha=0.26,
        linewidth=0.8,
    )

    ax.tick_params(
        axis="x",
        colors=BRAND_COLORS["text_body"],
        labelsize=9,
    )

    ax.tick_params(
        axis="y",
        colors=BRAND_COLORS["text_main"],
        labelsize=8,
    )

    for spine in ax.spines.values():
        spine.set_color(BRAND_COLORS["border"])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar, value in zip(bars, profile_df["percentile"]):
        x_pos = min(value + 1.5, 97)

        ax.text(
            x_pos,
            bar.get_y() + bar.get_height() / 2,
            f"{int(value) if float(value).is_integer() else value:.1f}".rstrip("0").rstrip("."),
            va="center",
            ha="left" if value < 92 else "right",
            color=BRAND_COLORS["text_body"],
            fontsize=8,
            weight="bold",
        )

    footer_mode = "vs Position" if mode == "position" else "vs All Players"

    footer_text = (
        f"Percentile Rank ({footer_mode}) | "
        f"Compared to {metadata['total_players_comparison']} "
        f"{metadata['comparison_group']} players | "
        f"{metadata['minimum_minutes_played']}+ minutes"
    )

    fig.text(
        0.5,
        0.01,
        footer_text,
        ha="center",
        fontsize=9,
        color=BRAND_COLORS["text_muted"],
    )

    plt.tight_layout(rect=[0, 0.04, 1, 1])

    return fig, metadata