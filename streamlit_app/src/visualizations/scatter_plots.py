from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# Player development scatter
# =============================================================================

def plot_player_development_scatter(
    df: pd.DataFrame,
    player_name: str,
    x_metric: str,
    y_metric: str,
    minimum_minutes_played: int | None = None,
    comparison_positions: list[str] | None = None,
    season_column: str = "season",
    player_column: str = "player",
    position_column: str = "position",
    minutes_column: str = "minutes_played",
):
    """
    Create a scatter chart comparing a player's development across two seasons.

    This chart:
    - resolves the player's comparison group automatically;
    - plots the comparison pool as background points;
    - highlights the selected player's previous and current season;
    - draws an arrow from the older season to the newer season;
    - returns a Matplotlib figure for Streamlit rendering.
    """
    position_column = _resolve_position_column(
        df=df,
        position_column=position_column,
    )

    if comparison_positions is None:
        player_position = _get_player_position(
            df=df,
            player_name=player_name,
            player_column=player_column,
            position_column=position_column,
        )

        comparison_positions = get_comparison_positions_for_position(
            position=player_position,
        )

    plot_df = _prepare_scatter_df(
        df=df,
        x_metric=x_metric,
        y_metric=y_metric,
        minimum_minutes_played=minimum_minutes_played,
        comparison_positions=comparison_positions,
        position_column=position_column,
        minutes_column=minutes_column,
    )

    player_df = plot_df[
        plot_df[player_column].eq(player_name)
    ].copy()

    player_df = player_df.sort_values(season_column)

    if len(player_df) < 2:
        raise ValueError(
            "The selected player needs at least two seasons for this chart."
        )

    player_previous = player_df.iloc[-2]
    player_current = player_df.iloc[-1]

    fig, ax = plt.subplots(figsize=(9, 6.2), dpi=150)
    fig.patch.set_facecolor(BRAND_COLORS["background_main"])
    ax.set_facecolor(BRAND_COLORS["background_main"])

    background_color_map = {
        "2024-25": CHART_COLORS.get("background_old_season", "#FACC15"),
        "2025": CHART_COLORS.get("background_old_season", "#FACC15"),
        "2025-26": CHART_COLORS.get("background_new_season", "#F43F5E"),
        "2026": CHART_COLORS.get("background_new_season", "#F43F5E"),
    }

    for season, group_df in plot_df.groupby(season_column):
        # group_sizes = _get_marker_sizes(
        #     df=group_df,
        #     minutes_column=minutes_column,
        #     divisor=8,
        #     minimum=30,
        #     maximum=300,
        # )
        group_sizes = 120

        label = str(season)

        ax.scatter(
            group_df[x_metric],
            group_df[y_metric],
            s=group_sizes,
            alpha=0.26,
            color=background_color_map.get(
                str(season),
                CHART_COLORS.get("neutral", "#64748B"),
            ),
            edgecolors="none",
            label=label,
            zorder=1,
        )

    previous_size = max(
        80,
        float(player_previous.get(minutes_column, 0)) / 20,
    )

    current_size = max(
        80,
        float(player_current.get(minutes_column, 0)) / 20,
    )

    ax.scatter(
        player_previous[x_metric],
        player_previous[y_metric],
        s=previous_size,
        color=CHART_COLORS.get("highlight_old", "#38BDF8"),
        edgecolors=BRAND_COLORS["text_main"],
        linewidths=1.2,
        zorder=5,
        label=f"{player_name} {player_previous[season_column]}",
    )

    ax.scatter(
        player_current[x_metric],
        player_current[y_metric],
        s=current_size,
        color=CHART_COLORS.get("highlight_new", "#34D399"),
        edgecolors=BRAND_COLORS["text_main"],
        linewidths=1.2,
        zorder=6,
        label=f"{player_name} {player_current[season_column]}",
    )

    ax.annotate(
        "",
        xy=(player_current[x_metric], player_current[y_metric]),
        xytext=(player_previous[x_metric], player_previous[y_metric]),
        arrowprops=dict(
            arrowstyle="->",
            color=CHART_COLORS.get("arrow", "#F59E0B"),
            lw=2.2,
        ),
        zorder=4,
    )

    y_range = plot_df[y_metric].max() - plot_df[y_metric].min()
    label_offset = y_range * 0.035 if y_range else 0.25

    ax.text(
        player_previous[x_metric],
        player_previous[y_metric] + label_offset,
        "",
        color=CHART_COLORS.get("highlight_old", "#38BDF8"),
        fontsize=10,
        weight="bold",
        ha="center",
    )

    ax.text(
        player_current[x_metric],
        player_current[y_metric] + label_offset,
        "",
        color=CHART_COLORS.get("highlight_new", "#34D399"),
        fontsize=10,
        weight="bold",
        ha="center",
    )

    _style_scatter_axis(
        ax=ax,
        title=f"{player_name} | Development Scatter",
        x_metric=x_metric,
        y_metric=y_metric,
    )

    _style_legend(ax)

    plt.tight_layout()

    return fig

# =============================================================================
# Player same-season scatter
# =============================================================================

def plot_player_season_scatter(
    df: pd.DataFrame,
    player_name: str,
    x_metric: str,
    y_metric: str,
    selected_season: str,
    minimum_minutes_played: int | None = None,
    comparison_positions: list[str] | None = None,
    season_column: str = "season",
    player_column: str = "player",
    position_column: str = "position",
    minutes_column: str = "minutes_played",
):
    """
    Create a scatter chart comparing a player within one selected season.

    This chart:
    - filters the dataframe to the selected season;
    - resolves the player's comparison group automatically;
    - plots the comparison pool as background points;
    - highlights the selected player;
    - adds X/Y league mean reference lines;
    - returns a Matplotlib figure for Streamlit rendering.
    """
    position_column = _resolve_position_column(
        df=df,
        position_column=position_column,
    )

    season_df = df[
        df[season_column].astype(str).eq(str(selected_season))
    ].copy()

    if comparison_positions is None:
        player_position = _get_player_position(
            df=season_df,
            player_name=player_name,
            player_column=player_column,
            position_column=position_column,
            season_column=season_column,
            selected_season=selected_season,
        )

        comparison_positions = get_comparison_positions_for_position(
            position=player_position,
        )

    plot_df = _prepare_scatter_df(
        df=season_df,
        x_metric=x_metric,
        y_metric=y_metric,
        minimum_minutes_played=minimum_minutes_played,
        comparison_positions=comparison_positions,
        position_column=position_column,
        minutes_column=minutes_column,
    )
    
    if plot_df.empty:
        raise ValueError(
            f"No valid data found for season {selected_season}."
        )

    player_df = plot_df[
        plot_df[player_column].eq(player_name)
    ].copy()

    if player_df.empty:
        raise ValueError(
            f"{player_name} was not found in season {selected_season}."
        )

    player_row = player_df.iloc[0]
    player_league = player_row["league_name"]

    fig, ax = plt.subplots(figsize=(9, 6.2), dpi=150)
    fig.patch.set_facecolor(BRAND_COLORS["background_main"])
    ax.set_facecolor(BRAND_COLORS["background_main"])

    # =========================
    # Background comparison pool
    # =========================

    background_sizes = _get_marker_sizes(
        df=plot_df,
        minutes_column=minutes_column,
        divisor=8,
        minimum=30,
        maximum=300,
    )

    # Keep fixed size if preferred for readability
    background_sizes = 120

    ax.scatter(
        plot_df[x_metric],
        plot_df[y_metric],
        s=background_sizes,
        alpha=0.35,
        color=CHART_COLORS.get("background_new_season", "#64748B"),
        edgecolors="none",
        label=f"{selected_season} comparison pool",
        zorder=1,
    )

    # =========================
    # League mean reference lines
    # =========================

    league_x_mean = plot_df[x_metric].mean()
    league_y_mean = plot_df[y_metric].mean()

    ax.axvline(
        x=league_x_mean,
        color="#FFFFFF",
        linestyle="--",
        linewidth=1.4,
        alpha=0.25,
        zorder=2,
        label="Mean",
    )

    ax.axhline(
        y=league_y_mean,
        color="#FFFFFF",
        linestyle="--",
        linewidth=1.4,
        alpha=0.35,
        zorder=2,
    )

    # x_min = plot_df[x_metric].min()
    # x_max = plot_df[x_metric].max()
    y_min = plot_df[y_metric].min()
    y_max = plot_df[y_metric].max()

    # x_range = x_max - x_min
    y_range = y_max - y_min

    # x_offset = x_range * 0.012 if x_range else 0.1
    # y_offset = y_range * 0.025 if y_range else 0.1

    # ax.text(
    #     league_x_mean + x_offset,
    #     y_max - y_offset,
    #     f"Mean {_get_feature_label(x_metric)}",
    #     color="#FFFFFF",
    #     fontsize=8.5,
    #     weight="bold",
    #     ha="left",
    #     va="top",
    #     zorder=6,
    # )

    # ax.text(
    #     x_min + x_offset,
    #     league_y_mean + y_offset,
    #     f"Mean {_get_feature_label(y_metric)}",
    #     color="#FFFFFF",
    #     fontsize=8.5,
    #     weight="bold",
    #     ha="left",
    #     va="bottom",
    #     zorder=6,
    # )

    # =========================
    # Highlight selected player
    # =========================

    player_size = max(
        110,
        float(player_row.get(minutes_column, 0)) / 10,
    )

    # Keep fixed size if preferred for readability
    player_size = 180

    ax.scatter(
        player_row[x_metric],
        player_row[y_metric],
        s=player_size,
        color=CHART_COLORS.get("highlight_new", "#2563EB"),
        edgecolors=BRAND_COLORS["text_main"],
        linewidths=1.3,
        zorder=5,
        label=f"{player_name}",
    )

    label_offset = y_range * 0.035 if y_range else 0.25

    ax.text(
        player_row[x_metric],
        player_row[y_metric] + label_offset,
        player_name,
        color=BRAND_COLORS["text_main"],
        fontsize=10,
        weight="bold",
        ha="center",
        zorder=6,
    )

    # =========================
    # Axis styling
    # =========================

    _style_scatter_axis(
        ax=ax,
        title=f"{player_name} | {player_league} - {selected_season}",
        x_metric=x_metric,
        y_metric=y_metric,
    )

    _style_legend(ax)

    plt.tight_layout()

    return fig

# =============================================================================
# Internal helpers
# =============================================================================

def get_comparison_group_for_position(position: str) -> str:
    position = str(position).strip().upper()

    return POSITION_TO_COMPARISON_GROUP.get(position, position)


def get_comparison_positions_for_position(position: str) -> list[str]:
    position = str(position).strip().upper()
    comparison_group = get_comparison_group_for_position(position)

    return COMPARISON_GROUPS.get(comparison_group, [position])


def _resolve_position_column(
    df: pd.DataFrame,
    position_column: str,
) -> str:
    if position_column in df.columns:
        return position_column

    if "main_position" in df.columns:
        return "main_position"

    if "position" in df.columns:
        return "position"

    raise KeyError(
        "No valid position column found. Expected one of: "
        f"'{position_column}', 'main_position', or 'position'."
    )


def _get_player_position(
    df: pd.DataFrame,
    player_name: str,
    player_column: str,
    position_column: str,
    season_column: str | None = None,
    selected_season: str | None = None,
) -> str:
    player_df = df[
        df[player_column].eq(player_name)
    ].copy()

    if selected_season is not None and season_column in player_df.columns:
        player_df = player_df[
            player_df[season_column].astype(str).eq(str(selected_season))
        ].copy()

    if player_df.empty:
        raise ValueError(
            f"Could not find player '{player_name}' to resolve comparison positions."
        )

    position = player_df.iloc[0].get(position_column)

    if pd.isna(position):
        raise ValueError(
            f"Player '{player_name}' has no valid position in column '{position_column}'."
        )

    return str(position).strip().upper()

def _get_feature_label(metric: str) -> str:
    return FEATURE_LABELS.get(metric, metric)


def _prepare_scatter_df(
    df: pd.DataFrame,
    x_metric: str,
    y_metric: str,
    minimum_minutes_played: int | None = None,
    comparison_positions: list[str] | None = None,
    position_column: str = "position",
    minutes_column: str = "minutes_played",
) -> pd.DataFrame:
    plot_df = df.copy()

    position_column = _resolve_position_column(
        df=plot_df,
        position_column=position_column,
    )

    if comparison_positions:
        plot_df = plot_df[
            plot_df[position_column].astype(str).str.upper().isin(comparison_positions)
        ].copy()

    if minimum_minutes_played is not None and minutes_column in plot_df.columns:
        plot_df = plot_df[
            plot_df[minutes_column] >= minimum_minutes_played
        ].copy()

    plot_df[x_metric] = pd.to_numeric(plot_df[x_metric], errors="coerce")
    plot_df[y_metric] = pd.to_numeric(plot_df[y_metric], errors="coerce")

    plot_df = plot_df.dropna(subset=[x_metric, y_metric])

    return plot_df.reset_index(drop=True)
    # plot_df = df.copy()

    # if comparison_positions:
    #     plot_df = plot_df[
    #         plot_df[position_column].isin(comparison_positions)
    #     ].copy()

    # if minimum_minutes_played is not None and minutes_column in plot_df.columns:
    #     plot_df = plot_df[
    #         plot_df[minutes_column] >= minimum_minutes_played
    #     ].copy()

    # plot_df[x_metric] = pd.to_numeric(plot_df[x_metric], errors="coerce")
    # plot_df[y_metric] = pd.to_numeric(plot_df[y_metric], errors="coerce")

    # plot_df = plot_df.dropna(subset=[x_metric, y_metric])

    # return plot_df.reset_index(drop=True)


def _get_marker_sizes(
    df: pd.DataFrame,
    minutes_column: str = "minutes_played",
    divisor: int = 8,
    minimum: int = 30,
    maximum: int = 300,
) -> pd.Series:
    if minutes_column not in df.columns:
        return pd.Series([minimum] * len(df), index=df.index)

    sizes = df[minutes_column].fillna(0) / divisor

    return sizes.clip(lower=minimum, upper=maximum)


def _style_scatter_axis(
    ax,
    title: str,
    x_metric: str,
    y_metric: str,
) -> None:
    ax.set_xlabel(
        _get_feature_label(x_metric),
        color=BRAND_COLORS["text_main"],
        fontsize=12,
        labelpad=10,
    )

    ax.set_ylabel(
        _get_feature_label(y_metric),
        color=BRAND_COLORS["text_main"],
        fontsize=12,
        labelpad=10,
    )

    ax.set_title(
        title,
        color=BRAND_COLORS["text_main"],
        fontsize=16,
        weight="bold",
        pad=14,
    )

    ax.grid(
        True,
        color=BRAND_COLORS["border"],
        alpha=0.3,
        linewidth=0.8,
    )

    for spine in ax.spines.values():
        spine.set_color(BRAND_COLORS["border"])

    ax.tick_params(colors=BRAND_COLORS["text_body"])


def _style_legend(ax) -> None:
    legend = ax.legend(frameon=False, fontsize=10, loc="best")

    if legend:
        for text in legend.get_texts():
            text.set_color(BRAND_COLORS["text_body"])

# =============================================================================
# Position comparison groups
# =============================================================================

POSITION_TO_ROLE = {
    "GK": "GK",

    "CB": "CB",
    "CCB": "CB",
    "LCB": "CB",
    "RCB": "CB",

    "LB": "FB",
    "RB": "FB",
    "LWB": "FB",
    "RWB": "FB",

    "DMF": "DM",
    "LDMF": "DM",
    "RDMF": "DM",

    "LCMF": "CM",
    "RCMF": "CM",
    "CMF": "CM",

    "AMF": "AM",

    "LAMF": "WINGER",
    "RAMF": "WINGER",
    "LW": "WINGER",
    "RW": "WINGER",
    "LWF": "WINGER",
    "RWF": "WINGER",

    "CF": "CF",
}


COMPARISON_GROUPS = {
    "GK": ["GK"],
    "CB": ["CB", "CCB", "LCB", "RCB"],
    "LB_LWB": ["LB", "LWB"],
    "RB_RWB": ["RB", "RWB"],
    "DM": ["DMF", "LDMF", "RDMF"],
    "CM": ["CMF", "LCMF", "RCMF"],
    "AM": ["AMF"],
    "LWF": ["LW", "LWF", "LAMF"],
    "RWF": ["RW", "RWF", "RAMF"],
    "CF": ["CF"],
}


POSITION_TO_COMPARISON_GROUP = {
    position: group_name
    for group_name, positions in COMPARISON_GROUPS.items()
    for position in positions
}
            
# COLORS
BRAND_COLORS = {
    "background_main": "#0F172A",
    "background_panel": "#1E293B",
    "text_main": "#E2E8F0",
    "text_body": "#CBD5E1",
    "text_muted": "#94A3B8",
    "border": "#475569",
}

CHART_COLORS = {
    "neutral": "#64748B",

    # Strong highlight colors
    "highlight_new": "#2563EB",  # strong blue
    "highlight_old": "#16A34A",  # strong green

    "arrow": "#F59E0B",

    "background_old_season": "#FACC15",
    "background_new_season": "#F43F5E",
}


FEATURE_LABELS = {
    # =================
    # General / Metadata
    # =================
    "matches_played": "Matches Played",
    "minutes_played": "Minutes Played",
    "age": "Age",
    "height": "Height",
    "weight": "Weight",
    "market_value": "Market Value",

    # =================
    # Shooting / Box Threat
    # =================
    "goals": "Goals",
    "goals_per_90": "Goals /90",
    "xg": "xG",
    "xg_per_90": "xG /90",
    "shots": "Shots",
    "shots_per_90": "Shots /90",
    "shots_on_target_%": "Shots On Target %",
    "goal_conversion_%": "Goal Conversion %",
    "non-penalty_goals": "Non-Penalty Goals",
    "non-penalty_goals_per_90": "Non-Penalty Goals /90",
    "non_penalty_xg": "Non-Penalty xG",
    "non_penalty_xg_per_90": "Non-Penalty xG /90",
    "touches_in_box_per_90": "Touches In Box /90",
    "head_goals": "Head Goals",
    "head_goals_per_90": "Head Goals /90",
    "penalties_taken": "Penalties Taken",
    "penalty_conversion_%": "Penalty Conversion %",

    # =================
    # Creativity / Chance Creation
    # =================
    "assists": "Assists",
    "assists_per_90": "Assists /90",
    "xa": "xA",
    "xa_per_90": "xA /90",
    "xa_per_100_passes": "xA / 100 Passes",
    "shot_assists_per_90": "Shot Assists /90",
    "key_passes_per_90": "Key Passes /90",
    "key_passes_per_100_passes": "Key Passes / 100 Passes",
    "smart_passes_per_90": "Smart Passes /90",
    "accurate_smart_passes_%": "Accurate Smart Passes %",
    "through_passes_per_90": "Through Passes /90",
    "accurate_through_passes_%": "Accurate Through Passes %",
    "second_assists_per_90": "Second Assists /90",
    "third_assists_per_90": "Third Assists /90",

    # =================
    # General Passing / Distribution
    # =================
    "passes_per_90": "Passes /90",
    "accurate_passes_%": "Accurate Passes %",
    "forward_passes_per_90": "Forward Passes /90",
    "accurate_forward_passes_%": "Accurate Forward Passes %",
    "back_passes_per_90": "Back Passes /90",
    "accurate_back_passes_%": "Accurate Back Passes %",
    "lateral_passes_per_90": "Lateral Passes /90",
    "accurate_lateral_passes_%": "Accurate Lateral Passes %",
    "short_/_medium_passes_per_90": "Short / Medium Passes /90",
    "accurate_short_/_medium_passes_%": "Accurate Short / Medium Passes %",
    "received_passes_per_90": "Received Passes /90",
    "received_long_passes_per_90": "Received Long Passes /90",
    "average_pass_length_m": "Average Pass Length M",

    # =================
    # Progression / Penetration
    # =================
    "progressive_passes_per_90": "Progressive Passes /90",
    "accurate_progressive_passes_%": "Accurate Progressive Passes %",
    "progressive_runs_per_90": "Progressive Runs /90",
    "passes_to_final_third_per_90": "Passes To Final Third /90",
    "accurate_passes_to_final_third_%": "Accurate Passes To Final Third %",
    "passes_to_penalty_area_per_90": "Passes To Penalty Area /90",
    "accurate_passes_to_penalty_area_%": "Accurate Passes To Penalty Area %",
    "deep_completions_per_90": "Deep Completions /90",

    # =================
    # Long Passing
    # =================
    "long_passes_per_90": "Long Passes /90",
    "accurate_long_passes_%": "Accurate Long Passes %",
    "average_long_pass_length_m": "Average Long Pass Length M",

    # =================
    # Crossing / Delivery
    # =================
    "crosses_per_90": "Crosses /90",
    "accurate_crosses_%": "Accurate Crosses %",
    "crosses_from_left_flank_per_90": "Crosses From Left Flank /90",
    "accurate_crosses_from_left_flank_%": "Accurate Crosses From Left Flank %",
    "crosses_from_right_flank_per_90": "Crosses From Right Flank /90",
    "accurate_crosses_from_right_flank_%": "Accurate Crosses From Right Flank %",
    "crosses_to_goalie_box_per_90": "Crosses To Goalie Box /90",
    "deep_completed_crosses_per_90": "Deep Completed Crosses /90",

    # =================
    # Dribbling / 1v1 Ability
    # =================
    "dribbles_per_90": "Dribbles /90",
    "successful_dribbles_%": "Successful Dribbles %",
    "offensive_duels_per_90": "Offensive Duels /90",
    "offensive_duels_won_%": "Offensive Duels Won %",
    "successful_attacking_actions_per_90": "Successful Attacking Actions /90",
    "fouls_suffered_per_90": "Fouls Suffered /90",
    "accelerations_per_90": "Accelerations /90",

    # =================
    # Duels / Physical Contest
    # =================
    "duels_per_90": "Duels /90",
    "duels_won_%": "Duels Won %",

    # =================
    # Defending / Discipline
    # =================
    "successful_defensive_actions_per_90": "Successful Defensive Actions /90",
    "defensive_duels_per_90": "Defensive Duels /90",
    "defensive_duels_won_%": "Defensive Duels Won %",
    "interceptions_per_90": "Interceptions /90",
    "padj_interceptions": "PAdj Interceptions",
    "p_adj_interceptions": "PAdj Interceptions",
    "shots_blocked_per_90": "Shots Blocked /90",
    "sliding_tackles_per_90": "Sliding Tackles /90",
    "padj_sliding_tackles": "PAdj Sliding Tackles",
    "p_adj_sliding_tackles": "PAdj Sliding Tackles",
    "fouls_per_90": "Fouls /90",
    "yellow_cards": "Yellow Cards",
    "yellow_cards_per_90": "Yellow Cards /90",
    "red_cards": "Red Cards",
    "red_cards_per_90": "Red Cards /90",

    # =================
    # Aerial Ability
    # =================
    "aerial_duels_per_90": "Aerial Duels /90",
    "aerial_duels_won_%": "Aerial Duels Won %",

    # =================
    # Set Pieces
    # =================
    "free_kicks_per_90": "Free Kicks /90",
    "direct_free_kicks_per_90": "Direct Free Kicks /90",
    "direct_free_kicks_on_target_%": "Direct Free Kicks On Target %",
    "corners_per_90": "Corners /90",

    # =================
    # Goalkeeper
    # =================
    "conceded_goals": "Conceded Goals",
    "conceded_goals_per_90": "Conceded Goals /90",
    "shots_against": "Shots Against",
    "shots_against_per_90": "Shots Against /90",
    "clean_sheets": "Clean Sheets",
    "save_rate_%": "Save Rate %",
    "xg_against": "xG Against",
    "xg_against_per_90": "xG Against /90",
    "prevented_goals": "Prevented Goals",
    "prevented_goals_per_90": "Prevented Goals /90",
    "back_passes_received_as_gk_per_90": "Back Passes Received As GK /90",
    "exits_per_90": "Exits /90",
    "aerial_duels_per_90.1": "Aerial Duels /90.1",
    "aerial_duels_per_90_1": "Aerial Duels /90.1",
}