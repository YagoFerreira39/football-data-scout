# =========================
# PLAY STYLE PROFILE UI
# =========================

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.services.play_style_profile_service import (
    get_league_play_style_distribution,
    get_play_style_profile_team_options,
    get_selected_team_play_style_profile,
)
from src.ui.team_header import render_team_header_from_row


# =========================
# DISPLAY HELPERS
# =========================

def _format_display_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rounds numeric columns for display.
    """

    view = df.copy()

    numeric_cols = view.select_dtypes(include="number").columns

    for col in numeric_cols:
        view[col] = view[col].round(1)

    return view


def _get_selected_team_title(profile_df: pd.DataFrame) -> str:
    """
    Builds chart title from profile data.
    """

    if profile_df.empty:
        return "Play Style Profile"

    row = profile_df.iloc[0]

    return (
        f"{row['team_name']} style of play\n"
        f"{row['team_name']} | {row['league_name']} {row['season']}"
    )


# =========================
# PLOT
# =========================

def plot_bipolar_play_style_profile(
    profile_df: pd.DataFrame,
    *,
    distribution_df: pd.DataFrame | None = None,
    show_league_distribution: bool = True,
):
    """
    Plots a report-style bipolar play-style profile.

    0 means closer to the left label.
    100 means closer to the right label.
    """

    from src.config.visual_theme import APP_THEME

    chart_df = profile_df.copy()

    if chart_df.empty:
        raise ValueError("Cannot plot an empty play-style profile.")

    chart_df = chart_df.reset_index(drop=True)

    y_positions = list(range(len(chart_df)))[::-1]

    team_name = chart_df["team_name"].iloc[0]
    league_name = chart_df["league_name"].iloc[0]
    season = chart_df["season"].iloc[0]

    fig_height = max(5.8, len(chart_df) * 0.95)

    fig, ax = plt.subplots(figsize=(11.5, fig_height))

    # =========================
    # Theme
    # =========================

    fig.patch.set_facecolor(APP_THEME["background"])
    ax.set_facecolor(APP_THEME["background"])

    plt.rcParams["font.family"] = APP_THEME["font_family"]

    # =========================
    # Background row lines
    # =========================

    for y_pos in y_positions:
        ax.hlines(
            y=y_pos,
            xmin=0,
            xmax=100,
            linewidth=1.4,
            color=APP_THEME["line"],
            alpha=0.55,
            zorder=1,
        )

    # =========================
    # League distribution
    # =========================

    if (
        show_league_distribution
        and distribution_df is not None
        and not distribution_df.empty
    ):
        for y_pos, dimension_key in zip(
            y_positions,
            chart_df["dimension_key"].tolist(),
        ):
            dimension_distribution = distribution_df[
                distribution_df["dimension_key"] == dimension_key
            ]

            ax.scatter(
                dimension_distribution["score"],
                [y_pos] * len(dimension_distribution),
                s=46,
                color=APP_THEME["league_distribution"],
                alpha=0.22,
                linewidths=0,
                zorder=2,
            )

    # =========================
    # League average marker
    # =========================

    ax.scatter(
        chart_df["league_average"],
        y_positions,
        marker="|",
        s=580,
        color=APP_THEME["league_average"],
        linewidths=2.6,
        alpha=0.95,
        label="League average",
        zorder=4,
    )

    # =========================
    # Selected team marker
    # =========================

    ax.scatter(
        chart_df["team_score"],
        y_positions,
        marker="h",
        s=440,
        color=APP_THEME["selected_team"],
        edgecolors=APP_THEME["background"],
        linewidths=1.5,
        alpha=1,
        label=team_name,
        zorder=5,
    )

    # =========================
    # Labels
    # =========================

    for y_pos, row in zip(y_positions, chart_df.itertuples()):
        ax.text(
            -2,
            y_pos + 0.23,
            row.left_label,
            ha="left",
            va="bottom",
            fontsize=10.5,
            color=APP_THEME["muted_text"],
        )

        ax.text(
            50,
            y_pos + 0.32,
            row.category.upper(),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color=APP_THEME["text"],
        )

        ax.text(
            102,
            y_pos + 0.23,
            row.right_label,
            ha="right",
            va="bottom",
            fontsize=10.5,
            color=APP_THEME["muted_text"],
        )

    # =========================
    # Header
    # =========================

    ax.text(
        0,
        len(chart_df) + 0.22,
        f"{team_name} style of play",
        ha="left",
        va="bottom",
        fontsize=20,
        fontweight="bold",
        color=APP_THEME["text"],
    )

    ax.text(
        0,
        len(chart_df) - 0.12,
        f"{league_name} | {season} | Scores relative to league",
        ha="left",
        va="bottom",
        fontsize=11.5,
        color=APP_THEME["muted_text"],
    )

    # =========================
    # Axis styling
    # =========================

    ax.set_xlim(-5, 105)
    ax.set_ylim(-0.8, len(chart_df) + 0.75)

    ax.set_yticks([])

    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(
        ["0", "25", "50", "75", "100"],
        color=APP_THEME["subtle_text"],
        fontsize=10,
    )

    ax.set_xlabel(
        "Style tendency",
        color=APP_THEME["muted_text"],
        fontsize=10.5,
        labelpad=10,
    )

    ax.grid(
        axis="x",
        linestyle="--",
        color=APP_THEME["grid"],
        alpha=0.28,
        linewidth=0.8,
    )

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(
        axis="x",
        colors=APP_THEME["muted_text"],
        length=0,
    )

    # =========================
    # Footer / legend
    # =========================

    legend = ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, -0.18),
        ncol=2,
        frameon=False,
        fontsize=10.5,
    )

    for text in legend.get_texts():
        text.set_color(APP_THEME["muted_text"])

    ax.text(
        0,
        -1.12,
        "0 = closer to left pole | 100 = closer to right pole",
        ha="left",
        va="center",
        fontsize=9.5,
        color=APP_THEME["muted_text"],
    )

    plt.tight_layout()

    return fig

# =========================
# STREAMLIT SECTION
# =========================

def render_play_style_profile_section(
    *,
    full_team_style_df: pd.DataFrame,
    filtered_team_style_df: pd.DataFrame,
) -> None:
    """
    Renders the bipolar play-style profile section.
    """

    st.subheader("Play Style Profile")

    if filtered_team_style_df.empty:
        st.info("No teams available for the selected filters.")
        return

    if full_team_style_df.empty:
        st.info("No team style data available.")
        return

    team_options_df = get_play_style_profile_team_options(
        filtered_team_style_df,
    )

    if team_options_df.empty:
        st.info("No team options available.")
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_team_label = st.selectbox(
            "Select club",
            team_options_df["team_option_label"].tolist(),
            key="play_style_profile_team_selector",
        )

    with col2:
        show_league_distribution = st.toggle(
            "Show league dots",
            value=True,
            key="play_style_profile_show_distribution",
        )

    try:
        profile_df = get_selected_team_play_style_profile(
            full_team_style_df,
            team_option_label=selected_team_label,
        )
        if not profile_df.empty:
            render_team_header_from_row(profile_df.iloc[0], title_col="team_name")

        distribution_df = get_league_play_style_distribution(
            full_team_style_df,
            team_option_label=selected_team_label,
        )

    except Exception as exc:
        st.warning(f"Could not build play-style profile: {exc}")
        return

    fig = plot_bipolar_play_style_profile(
        profile_df,
        distribution_df=distribution_df,
        show_league_distribution=show_league_distribution,
    )

    st.pyplot(fig)

    st.caption(
        "Data-led style tendency chart. Scores are relative to the selected league-season. "
        "This describes profile shape, not team quality."
    )

    with st.expander("Show profile data"):
        display_cols = [
            "category",
            "left_label",
            "right_label",
            "team_score",
            "league_average",
            "difference_from_league_average",
            "league_rank",
            "league_teams",
            "available_weight",
            "used_metrics",
        ]

        available_cols = [
            col for col in display_cols
            if col in profile_df.columns
        ]

        st.dataframe(
            _format_display_df(profile_df[available_cols]),
            use_container_width=True,
            hide_index=True,
        )