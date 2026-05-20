from html import escape
from io import BytesIO
from textwrap import dedent

import pandas as pd
import streamlit as st

# TEST
import matplotlib.pyplot as plt
from mplsoccer import Pitch

from src.visualizations.pizza_charts import plot_player_profile
from src.visualizations.scatter_plots import plot_player_development_scatter, plot_player_season_scatter
from src.visualizations.bar_charts import plot_player_percentile_bar_chart
from src.visualizations.radar_charts import plot_player_raw_radar_chart, plot_players_raw_radar_comparison

# =========================
# Constants
# =========================

player_col = "player"
team_col = "team_within_selected_timeframe"
season_col = "season"
league_col = "league_name"
country_col = "league_country"
position_col = "position"
common_position_col = "common_position"
age_col = "age"
birth_country_col = "birth_country"
# passport_country_col = "passport_country"
foot_col = "foot"
height_col = "height"
weight_col = "weight"
contract_col = "contract_expires"
market_value_col = "market_value"
loan_col = "on_loan"

# =============================================================================
# RENDER COMPONENTS
# ============================================================================

# SIDEBAR FILTERS
def render_sidebar_filters() -> None:
    with st.sidebar:
        st.markdown("### Player Filters 2")

# PLAYER HEADER
def render_player_header(player_row: pd.Series, selected_season: str) -> None:
    player_name = get_value(player_row, player_col)
    team_name = get_value(player_row, team_col)
    # season = get_value(player_row, season_col)
    league_name = get_value(player_row, league_col)
    country_name = get_value(player_row, country_col)

    position = get_value(player_row, "main_position")

    st.markdown(
    f"""
<div class="player-profile-header">
    <div class="player-profile-header-content">
        <div>
            <div class="player-profile-kicker">Player Profile</div>
            <div class="player-profile-title">{escape(player_name)}</div>
            <div class="player-profile-meta">
                <span>{escape(team_name)}</span>
                <span>{escape(league_name)}</span>
                <span>{escape(country_name)}</span>
                <span>{escape(selected_season)}</span>
            </div>
        </div>
        <div class="player-profile-position">{escape(position)}</div>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)
    
# PLAYER BIO
def render_player_bio_strip(player_row: pd.Series) -> None:
    age = format_number(get_value(player_row, age_col))
    nationality = format_text(get_value(player_row, birth_country_col))
    foot = format_text(get_value(player_row, foot_col))
    height = format_height(get_value(player_row, height_col))
    weight = format_weight(get_value(player_row, weight_col))
    contract = format_text(get_value(player_row, contract_col))
    market_value = format_market_value(get_value(player_row, market_value_col))
    loan_status = format_text(get_value(player_row, loan_col))

    bio_items = [
        ("Age", age),
        ("Nationality", nationality),
        ("Foot", foot),
        ("Height", height),
        ("Weight", weight),
        ("Contract", contract),
        ("Market Value", market_value),
        ("Loan", loan_status),
    ]

    items_html = ""

    for label, value in bio_items:
        items_html += f"""
        <div class="player-bio-card">
            <div class="player-bio-label">{escape(str(label))}</div>
            <div class="player-bio-value">{escape(str(value))}</div>
        </div>
        """

    st.markdown(
        dedent(
        f"""
        <div class="player-bio-grid">
            {items_html}
        </div>
        """
        ).strip(),
        unsafe_allow_html=True,
    )
    
def build_general_stats(player_row: pd.Series) -> list[dict]:
    base_stats = [
        {
            "label": "Games Played",
            "value": format_number(get_value(player_row, "matches_played")),
        },
        {
            "label": "Minutes Played",
            "value": format_number(get_value(player_row, "minutes_played")),
        },
        {
            "label": "Market Value",
            "value": format_market_value(get_value(player_row, market_value_col)),
        },
    ]
    role_stats = []

    return base_stats + role_stats

def render_general_tab(player_row: pd.Series) -> None:
    general_stats = build_general_stats(player_row=player_row)

    st.markdown(
        tab_panel_html(
            title="General",
            description="",
            stats=general_stats,
            columns=3,
        ),
        unsafe_allow_html=True,
    )
    
def render_goalkeeping_tab(player_row: pd.Series) -> None:
    save_rate = get_value(player_row, "save_rate_%", 0)

    save_rate_html = circular_rate_html(
        label="Saves",
        value=save_rate,
    )

    main_cards = [
        {
            "label": "Clean sheets",
            "value": format_number(get_value(player_row, "clean_sheets")),
        },
        {
            "label": "Shots against",
            "value": format_number(get_value(player_row, "shots_against")),
        },
        {
            "label": "Shots against / 90",
            "value": format_number(get_value(player_row, "shots_against_per_90"), 2),
        },
        {
            "label": "Conceded goals",
            "value": format_number(get_value(player_row, "conceded_goals")),
        },
        {
            "label": "Conceded goals / 90",
            "value": format_number(get_value(player_row, "conceded_goals_per_90"), 2),
        },
        {
            "label": "xG against",
            "value": format_number(get_value(player_row, "xg_against"), 2),
        },
    ]

    main_cards_html = "\n".join(
        goalkeeping_detail_card_html(
            label=card["label"],
            value=card["value"],
        )
        for card in main_cards
    )

    secondary_cards = [
        {
            "label": "xG against / 90",
            "value": format_number(get_value(player_row, "xg_against_per_90"), 2),
        },
        {
            "label": "Prevented goals",
            "value": format_number(get_value(player_row, "prevented_goals"), 2),
        },
        # {
        #     "label": "Prevented goals / 90",
        #     "value": format_number(get_value(player_row, "prevented_goals_per_90"), 2),
        # },
        {
            "label": "Exits / 90",
            "value": format_number(get_value(player_row, "exits_per_90"), 2),
        },
        # {
        #     "label": "Back passes received / 90",
        #     "value": format_number(get_value(player_row, "back_passes_received_as_gk_per_90"), 2),
        # },
        {
            "label": "Aerial duels / 90",
            "value": format_number(get_value(player_row, "aerial_duels_per_90.1"), 2),
        },
    ]

    secondary_cards_html = "\n".join(
        goalkeeping_secondary_card_html(
            label=card["label"],
            value=card["value"],
        )
        for card in secondary_cards
    )

    html = dedent(
        f"""
<div class="goalkeeping-panel">
<div class="goalkeeping-panel-title">Goalkeeping</div>
<div class="goalkeeping-panel-description">
Shot-stopping, goal prevention and goalkeeper-specific involvement.
</div>

<div class="goalkeeping-main-grid">
<div class="goalkeeping-box">
<div class="goalkeeping-box-title">Save rate</div>
{save_rate_html}
</div>

<div class="goalkeeping-detail-grid">
{main_cards_html}
</div>
</div>

<div class="goalkeeping-secondary-grid">
{secondary_cards_html}
</div>
</div>
"""
    ).strip()

    st.markdown(html, unsafe_allow_html=True)
        
def render_attack_tab(player_row: pd.Series) -> None:
    shots = get_value(player_row, "shots", 0)
    shots_on_target_pct = get_value(player_row, "shots_on_target_%", 0)
    shots_per_90 = get_value(player_row, "shots_per_90", 0)
    goals = get_value(player_row, "goals", 0)
    non_penalty_goals = get_value(player_row, "non-penalty_goals", 0)

    shots_numeric = 0 if pd.isna(shots) else float(shots)
    goals_numeric = 0 if pd.isna(goals) else float(goals)
    non_penalty_goals_numeric = 0 if pd.isna(non_penalty_goals) else float(non_penalty_goals)
    shots_per_90_numeric = 0 if pd.isna(shots_per_90) else float(shots_per_90)
    shots_on_target_estimated = (
        shots_numeric * float(shots_on_target_pct) / 100
        if not pd.isna(shots_on_target_pct)
        else 0
    )

    max_bar_value = max(shots_numeric, shots_on_target_estimated, non_penalty_goals_numeric, goals_numeric, 1)

    bars_html = "\n".join(
        [
            attack_bar_row_html(
                label="Total shots",
                value=shots_numeric,
                max_value=max_bar_value,
            ),
            attack_bar_row_html(
                label="Shots on target",
                value=shots_on_target_estimated,
                max_value=max_bar_value,
            ),
            attack_bar_row_html(
                label="Goals scored",
                value=goals_numeric,
                max_value=max_bar_value,
            ),
            attack_bar_row_html(
                label="Non-penalty goals",
                value=non_penalty_goals_numeric,
                max_value=max_bar_value,
            ),
        ]
    )

    minutes_per_goal = float(get_value(player_row, "minutes_played")) / goals_numeric if goals_numeric > 0 else None
    efficiency_html = "\n".join(
        [
            attack_efficiency_card_html(
                label="Goal conversion",
                value=format_percent(get_value(player_row, "goal_conversion_%")),
            ),
            attack_efficiency_card_html(
                label="Minutes per goal",
                value=format_number(minutes_per_goal, 1) if minutes_per_goal is not None else "N/A",
            ),
        ]
    )

    detail_cards = [
        {
            "label": "Shots per 90",
            "value": format_number(get_value(player_row, "shots_per_90"), 2),
        },
        {
            "label": "Non-penalty goals / 90",
            "value": format_number(get_value(player_row, "non-penalty_goals_per_90"), 2),
        },
        {
            "label": "Non-penalty xG",
            "value": format_number(get_value(player_row, "non_penalty_xg"), 2),
        },
        {
            "label": "Headed Goals",
            "value": get_value(player_row, "head_goals"),
        },
    ]

    detail_html = "\n".join(
        attack_detail_card_html(
            label=card["label"],
            value=card["value"],
        )
        for card in detail_cards
    )

    html = f"""
<div class="attack-panel">
<div class="attack-panel-title">Attack</div>
<div class="attack-panel-description">
    Shot volume, scoring output and direct attacking threat.
</div>

<div class="attack-layout">
<div class="attack-box">
<div class="attack-box-title">Shooting volume</div>
    {bars_html}
</div>

<div class="attack-box">
<div class="attack-box-title">Efficiency</div>
<div class="attack-efficiency-grid">
    {efficiency_html}
</div>
</div>
</div>

<div class="attack-detail-grid">
    {detail_html}
</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)

def render_distribution_tab(player_row: pd.Series) -> None:
    passing_volume_html = "\n".join(
        [
            distribution_feature_row_html(
                label="Passes / 90",
                value=format_number(get_value(player_row, "passes_per_90"), 2),
            ),
            distribution_feature_row_html(
                label="Forward passes / 90",
                value=format_number(get_value(player_row, "forward_passes_per_90"), 2),
            ),
            distribution_feature_row_html(
                label="Long passes / 90",
                value=format_number(get_value(player_row, "long_passes_per_90"), 2),
            ),
        ]
    )

    progression_html = "\n".join(
        [
            distribution_feature_row_html(
                label="Progressive passes / 90",
                value=format_number(get_value(player_row, "progressive_passes_per_90"), 2),
            ),
            distribution_feature_row_html(
                label="Passes to final third / 90",
                value=format_number(get_value(player_row, "passes_to_final_third_per_90"), 2),
            ),
            distribution_feature_row_html(
                label="Passes to penalty area / 90",
                value=format_number(get_value(player_row, "passes_to_penalty_area_per_90"), 2),
            ),
        ]
    )

    creation_html = "\n".join(
        [
            distribution_feature_row_html(
                label="Key passes / 90",
                value=format_number(get_value(player_row, "key_passes_per_90"), 2),
            ),
            distribution_feature_row_html(
                label="xA / 90",
                value=format_number(get_value(player_row, "xa_per_90"), 2),
            ),
            distribution_feature_row_html(
                label="Shot assists / 90",
                value=format_number(get_value(player_row, "shot_assists_per_90"), 2),
            ),
        ]
    )
    
    accuracy_html = "\n".join([
        circular_rate_html("Pass Accuracy", get_value(player_row, "accurate_passes_%", 0)),
        circular_rate_html("Forward Pass Accuracy", get_value(player_row, "accurate_forward_passes_%", 0)),
        circular_rate_html("Long Pass Accuracy", get_value(player_row, "accurate_long_passes_%", 0)),
        circular_rate_html("Progressive Pass Accuracy", get_value(player_row, "accurate_progressive_passes_%", 0)),
    ])

    line_players_detail_cards = [
        {
            "label": "Smart passes / 90",
            "value": format_number(get_value(player_row, "smart_passes_per_90"), 2),
        },
        {
            "label": "Through passes / 90",
            "value": format_number(get_value(player_row, "through_passes_per_90"), 2),
        },
        {
            "label": "Deep completions / 90",
            "value": format_number(get_value(player_row, "deep_completions_per_90"), 2),
        },
        {
            "label": "Deep completed crosses / 90",
            "value": format_number(get_value(player_row, "deep_completed_crosses_per_90"), 2),
        },
        {
            "label": "Crosses / 90",
            "value": format_number(get_value(player_row, "crosses_per_90"), 2),
        },
        {
            "label": "Cross accuracy",
            "value": format_percent(get_value(player_row, "accurate_crosses_%")),
        },
        {
            "label": "xA / 100 passes",
            "value": format_number(get_value(player_row, "xa_per_100_passes"), 2),
        },
        {
            "label": "Key passes / 100 passes",
            "value": format_number(get_value(player_row, "key_passes_per_100_passes"), 2),
        },
    ]
    
    gk_detail_cards = []
    
    detail_cards = line_players_detail_cards if not is_goalkeeper(player_row) else gk_detail_cards

    detail_html = "\n".join(
        distribution_detail_card_html(
            label=card["label"],
            value=card["value"],
        )
        for card in detail_cards
    )
    
    creation_box_html = ""

    if not is_goalkeeper(player_row):
        creation_box_html = dedent(
        f"""
        <div class="distribution-box">
            <div class="distribution-box-title">Chance creation</div>
            {creation_html}
        </div>
        """
        ).strip()

    html = f"""
<div class="distribution-panel">
<div class="distribution-panel-title">Distribution</div>
<div class="distribution-panel-description">
Passing volume, progression, accuracy and chance creation.
</div>

<div class="distribution-main-grid">
{creation_box_html}
<div class="distribution-box">
    <div class="distribution-box-title">Passing volume</div>
    {passing_volume_html}
</div>

<div class="distribution-box">
    <div class="distribution-box-title">Progression</div>
    {progression_html}
</div>
</div>

<div class="distribution-rate-panel">
<div class="distribution-rate-grid">
    {accuracy_html}
</div>
</div>

<div class="distribution-detail-grid">
{detail_html}
</div>
</div>
"""

    st.markdown(html, unsafe_allow_html=True)
    
def render_defence_tab(player_row: pd.Series) -> None:
    defensive_actions_html = "\n".join(
        [
            defence_feature_row_html(
                label="Defensive actions / 90",
                value=format_number(
                    get_value(player_row, "successful_defensive_actions_per_90"),
                    2,
                ),
            ),
            defence_feature_row_html(
                label="Interceptions / 90",
                value=format_number(get_value(player_row, "interceptions_per_90"), 2),
            ),
            defence_feature_row_html(
                label="PAdj interceptions",
                value=format_number(get_value(player_row, "padj_interceptions"), 2),
            ),
            defence_feature_row_html(
                label="Shots blocked / 90",
                value=format_number(get_value(player_row, "shots_blocked_per_90"), 2),
            ),
        ]
    )

    duel_activity_html = "\n".join(
        [
            defence_feature_row_html(
                label="Defensive duels / 90",
                value=format_number(get_value(player_row, "defensive_duels_per_90"), 2),
            ),
            defence_feature_row_html(
                label="Aerial duels / 90",
                value=format_number(get_value(player_row, "aerial_duels_per_90"), 2),
            ),
            defence_feature_row_html(
                label="Sliding tackles / 90",
                value=format_number(get_value(player_row, "sliding_tackles_per_90"), 2),
            ),
            defence_feature_row_html(
                label="PAdj sliding tackles",
                value=format_number(get_value(player_row, "padj_sliding_tackles"), 2),
            ),
        ]
    )

    rates_html = "\n".join([
        circular_rate_html("Defensive duels", get_value(player_row, "defensive_duels_won_%", 0)),
        circular_rate_html("Aerial duels", get_value(player_row, "aerial_duels_won_%", 0)),
        circular_rate_html("Duels", get_value(player_row, "duels_won_%", 0)),
    ])
    # success_rates_html = "\n".join(
    #     [
    #         defence_rate_row_html(
    #             label="Defensive duels won",
    #             value=get_value(player_row, "defensive_duels_won_%", None),
    #         ),
    #         defence_rate_row_html(
    #             label="Aerial duels won",
    #             value=get_value(player_row, "aerial_duels_won_%", None),
    #         ),
    #         defence_rate_row_html(
    #             label="Duels won",
    #             value=get_value(player_row, "duels_won_%", None),
    #         ),
    #     ]
    # )

    detail_cards = [
        {
            "label": "Duels / 90",
            "value": format_number(get_value(player_row, "duels_per_90"), 2),
        },
        {
            "label": "Fouls / 90",
            "value": format_number(get_value(player_row, "fouls_per_90"), 2),
        },
        {
            "label": "Yellow cards",
            "value": format_number(get_value(player_row, "yellow_cards")),
        },
        {
            "label": "Red cards",
            "value": format_number(get_value(player_row, "red_cards")),
        },
        {
            "label": "Yellow cards / 90",
            "value": format_number(get_value(player_row, "yellow_cards_per_90"), 2),
        },
        {
            "label": "Red cards / 90",
            "value": format_number(get_value(player_row, "red_cards_per_90"), 2),
        },
        {
            "label": "Fouls suffered / 90",
            "value": format_number(get_value(player_row, "fouls_suffered_per_90"), 2),
        },
        {
            "label": "Aerial duels won",
            "value": format_percent(get_value(player_row, "aerial_duels_won_%")),
        },
    ]

    detail_html = "\n".join(
        defence_detail_card_html(
            label=card["label"],
            value=card["value"],
        )
        for card in detail_cards
    )

    html = dedent(
f"""
<div class="defence-panel">
<div class="defence-panel-title">Defence</div>
<div class="defence-panel-description">
Defensive activity, duel involvement, ball-winning output and discipline.
</div>

<div class="defence-main-grid">
<div class="defence-box">
<div class="defence-box-title">Defensive actions</div>
{defensive_actions_html}
</div>

<div class="defence-box">
<div class="defence-box-title">Duel activity</div>
{duel_activity_html}
</div>
</div>

<div class="defence-rate-panel">
<div class="defence-rate-grid">
{rates_html}
</div>
</div>

<div class="defence-detail-grid">
{detail_html}
</div>
</div>
"""
).strip()

    st.markdown(html, unsafe_allow_html=True)
    
def render_detailed_stats(
    player_row: pd.Series, 
    league_season_df: pd.DataFrame, 
    league_df:pd.DataFrame,
    selected_profile: str | None,
    minimum_minutes_played: int,
    selected_scatter_metrics
) -> None:
    gk_tabs = ["General", "Goalkeeping", "Distribution"]
    line_player_tabs = ["General", "Attack", "Distribution", "Defence"]
    
    is_gk = is_goalkeeper(player_row=player_row)
    
    if is_gk:
        tabs = st.tabs(gk_tabs)
    else:
        tabs = st.tabs(line_player_tabs)

    with tabs[0]:
        render_general_tab(player_row=player_row)
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        st.divider() 

        render_chart_section_title(
            title="Profile Charts",
            description="Role-based visual summaries using percentile and profile metrics.",
        )
        chart_col_1, chart_col_2 = st.columns([1, 1])
        with chart_col_1:    
            download_file_name = create_file_name_for_download(player_row=player_row, minimum_minutes=minimum_minutes_played, chart_type="pizza_chart")
            pizza_chart_fig = render_player_profile_chart(
                player_row=player_row, 
                league_season_df=league_season_df, 
                selected_profile=selected_profile,
                minimum_minutes_played=minimum_minutes_played
            )
            render_figure_with_download(
                fig=pizza_chart_fig,
                file_name=download_file_name,
                download_label="Download",
            )
            
        with chart_col_2:
            download_file_name = create_file_name_for_download(player_row=player_row, minimum_minutes=minimum_minutes_played, chart_type="bar_chart")
            bar_chart_fig = render_player_percentile_bar_chart(
                player_row=player_row,
                league_season_df=league_season_df,
                selected_profile=selected_profile,
                minimum_minutes_played=minimum_minutes_played
            )

            render_figure_with_download(
                fig=bar_chart_fig,
                file_name=download_file_name,
                download_label="Download",
            )
        
        st.divider() 

        render_chart_section_title(
            title="Radar Charts",
            description="",
        )
        radar_chart_col_1, radar_chart_col_2 = st.columns([1, 1])
        with radar_chart_col_1:
            download_file_name = create_file_name_for_download(player_row=player_row, minimum_minutes=minimum_minutes_played, chart_type="radar_chart")
            radar_chart_fig = render_player_radar_chart(
                player_row=player_row,
                league_season_df=league_season_df,
                selected_profile=selected_profile,
                minimum_minutes_played=minimum_minutes_played
            )
            render_figure_with_download(
                fig=radar_chart_fig,
                file_name=download_file_name,
                download_label="Download",
            )

        with radar_chart_col_2:
            pass
            
        st.divider()

        render_chart_section_title(
            title="Comparison Scatters",
            description="Compare the player against the league pool and track development across seasons.",
        )
        scatter_col_1, scatter_col_2 = st.columns([1, 1])
        with scatter_col_1:
            download_file_name = create_file_name_for_download(player_row=player_row, minimum_minutes=minimum_minutes_played, chart_type="season_scatter_chart")
            scatter_plot_fig_1 = render_player_season_scatter_plot(
                player_row=player_row, 
                league_season_df=league_season_df,
                selected_scatter_metrics=selected_scatter_metrics,
                minimum_minutes_played=minimum_minutes_played
            )
            render_figure_with_download(
                fig=scatter_plot_fig_1,
                file_name=download_file_name,
                download_label="Download"
            )
        
        should_display_player_development = len(league_df[league_df[player_col] == player_row.get(player_col, "")]) >= 2
        if should_display_player_development:
            with scatter_col_2:
                download_file_name = create_file_name_for_download(player_row=player_row, minimum_minutes=minimum_minutes_played, chart_type="development_scatter_chart")
                scatter_plot_fig_2 = render_player_development_scatter_plot(
                    player_row=player_row, 
                    player_multi_season_comparison_df=league_df,
                    selected_scatter_metrics=selected_scatter_metrics,
                    minimum_minutes_played=minimum_minutes_played
                )
                render_figure_with_download(
                    fig=scatter_plot_fig_2,
                    file_name=download_file_name,
                    download_label="Download"
                )
            
    with tabs[1]:
        render_general_tab(player_row=player_row)
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        if is_gk:
            render_goalkeeping_tab(player_row=player_row)
        else:
            render_attack_tab(player_row=player_row)
        
    with tabs[2]:
        render_general_tab(player_row=player_row)
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        render_distribution_tab(player_row=player_row)
    
    if not is_gk:
        with tabs[3]:
            render_general_tab(player_row=player_row)
            st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
            render_defence_tab(player_row=player_row)
            

# =============================================================================
# VISUALIZATION HELPERS
# ============================================================================

def figure_to_png_buffer(fig, dpi: int = 300) -> BytesIO:
    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=dpi,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )

    buffer.seek(0)
    return buffer

def create_file_name_for_download(player_row: pd.Series, minimum_minutes: int, chart_type: str) -> str:
    player_name = player_row["player_slug"]
    team = player_row["team_slug"]
    league = player_row["league_slug"]
    season = player_row[season_col]
    
    return f"{player_name}_{team}_{league}_{season}_{minimum_minutes}minutes_{chart_type}.png"

def render_figure_with_download(
    fig,
    file_name: str,
    download_label: str = "Download chart",
    dpi: int = 300,
    use_container_width: bool = True,
) -> None:
    st.pyplot(fig, use_container_width=use_container_width)

    buffer = figure_to_png_buffer(fig, dpi=dpi)

    st.download_button(
        label=download_label,
        data=buffer,
        file_name=file_name,
        mime="image/png",
        use_container_width=use_container_width,
    )

    plt.close(fig)
 
def render_player_profile_chart(
    player_row: pd.Series, 
    league_season_df: pd.DataFrame, 
    selected_profile: str | None,
    minimum_minutes_played: int
) -> None:
    player_name = get_value(player_row, player_col)
    # minimum_minutes = min(int(get_value(player_row, "minutes_played", 0)), 1000)
    profile = selected_profile or "attacking_midfielder"
    mode="position"
    
    fig, _ = plot_player_profile(
        df=league_season_df,
        player_names=player_name,
        minimum_minutes_played=minimum_minutes_played,
        profile=profile,
        mode=mode,
    )
    
    return fig

def render_player_percentile_bar_chart(
    player_row: pd.Series,
    league_season_df: pd.DataFrame,
    minimum_minutes_played: int,
    selected_profile: str | None = None,
):
    # minimum_minutes = min(int(get_value(player_row, "minutes_played", 0)), 1000)
    fig, _ = plot_player_percentile_bar_chart(
        df=league_season_df,
        player_name=player_row["player"],
        minimum_minutes_played=minimum_minutes_played,
        profile=selected_profile,
        mode="position",
        sort_values=True,
    )

    return fig

def render_player_radar_chart(
    player_row: pd.Series,
    league_season_df: pd.DataFrame,
    minimum_minutes_played: int,
    selected_profile: str | None = None,
):
    # minimum_minutes = min(int(get_value(player_row, "minutes_played", 0)), 1000)
    fig, _ = plot_player_raw_radar_chart(
        df=league_season_df,
        player_name=player_row["player"],
        minimum_minutes_played=minimum_minutes_played,
        profile=selected_profile,
        mode="position",
    )

    return fig

# def render_players_radar_comparison_chart(
#     player_name_1: str,
#     player_name_2: str,
#     league_season_df: pd.DataFrame,
#     selected_profile: str | None = None,
# ):
#     minimum_minutes = min(int(get_value(player_row, "minutes_played", 0)), 1000)
#     fig, _ = plot_player_raw_radar_chart(
#         df=league_season_df,
#         player_name_1=player_name_1,
#         player_name_2=player_name_2,
#         minimum_minutes_played=900,
#         profile=selected_profile,
#         mode="position",
#     )

#     return fig

def render_player_season_scatter_plot(
    player_row: pd.Series, 
    league_season_df: pd.DataFrame,
    selected_scatter_metrics,
    minimum_minutes_played: int
):
    # minimum_minutes = min(int(get_value(player_row, "minutes_played", 0)), 1000)
    fig = plot_player_season_scatter(
        df=league_season_df,
        player_name=get_value(player_row, player_col),
        x_metric=selected_scatter_metrics["x_metric"],
        y_metric=selected_scatter_metrics["y_metric"],
        selected_season=player_row["season"],
        minimum_minutes_played=minimum_minutes_played,
        position_column="main_position"
    )
    
    return fig

def render_player_development_scatter_plot(
    player_row: pd.Series, 
    player_multi_season_comparison_df: pd.DataFrame,
    selected_scatter_metrics,
    minimum_minutes_played: int
):
    # minimum_minutes = min(int(get_value(player_row, "minutes_played", 0)), 1000)
    fig = plot_player_development_scatter(
        df=player_multi_season_comparison_df,
        player_name=player_row["player"],
        x_metric=selected_scatter_metrics["x_metric"],
        y_metric=selected_scatter_metrics["y_metric"],
        minimum_minutes_played=minimum_minutes_played,
    )
    
    return fig

def render_chart_section_title(title: str, description: str | None = None) -> None:
    description_html = ""

    if description:
        description_html = f"""
        <div class="chart-section-description">{description}</div>
        """

    st.markdown(
        f"""
        <div class="chart-section-header">
            <div class="chart-section-title">{title}</div>
            {description_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
    

# =============================================================================
# Value formatting helpers
# =============================================================================

def format_number(value, decimals: int = 0, fallback: str = "-") -> str:
    if value is None or pd.isna(value):
        return fallback

    try:
        numeric_value = float(value)

        if decimals == 0:
            return f"{numeric_value:,.0f}"

        return f"{numeric_value:,.{decimals}f}"

    except (TypeError, ValueError):
        return fallback


def format_percent(value, decimals: int = 1, fallback: str = "-") -> str:
    if value is None or pd.isna(value):
        return fallback

    try:
        return f"{float(value):.{decimals}f}%"

    except (TypeError, ValueError):
        return fallback
    
def format_height(value) -> str:
    value = format_number(value)

    if value == "-":
        return "-"

    return f"{value} cm"


def format_weight(value) -> str:
    value = format_number(value)

    if value == "-":
        return "-"

    return f"{value} kg"


def format_text(value, fallback: str = "-") -> str:
    if value is None or pd.isna(value):
        return fallback

    value = str(value).strip()

    if not value or value.lower() in {"nan", "none"}:
        return fallback

    return value


def format_market_value(value, fallback: str = "-") -> str:
    if value is None or pd.isna(value):
        return fallback

    try:
        numeric_value = float(value)

        if numeric_value <= 0:
            return fallback

        if numeric_value >= 1_000_000:
            return f"€{numeric_value / 1_000_000:.1f}M"

        if numeric_value >= 1_000:
            return f"€{numeric_value / 1_000:.0f}K"

        return f"€{numeric_value:,.0f}"

    except (TypeError, ValueError):
        return format_text(value, fallback=fallback)
    
def get_value(row: pd.Series, column: str, fallback: str = "-") -> str:
    if column not in row.index:
        return fallback

    value = row[column]

    if pd.isna(value):
        return fallback

    value = str(value).strip()

    if not value or value.lower() in {"nan", "none"}:
        return fallback

    return value

def is_goalkeeper(player_row: pd.Series) -> bool:
    position = str(
        get_value(
            player_row,
            "common_position",
            get_value(player_row, "position", ""),
        )
    ).upper()

    return position == "GK"

# =============================================================================
# Generic metric/card HTML helpers
# =============================================================================

def metric_card_html(label: str, value: str, subtitle: str | None = None) -> str:
    subtitle_html = ""

    if subtitle:
        subtitle_html = dedent(
            f"""
            <div class="profile-metric-subtitle">{escape(str(subtitle))}</div>
            """
        ).strip()

    return dedent(
        f"""
<div class="profile-metric-card">
<div class="profile-metric-value">{escape(str(value))}</div>
<div class="profile-metric-label">{escape(str(label))}</div>
{subtitle_html}
</div>
"""
    ).strip()


def metric_grid_html(stats: list[dict], columns: int = 4) -> str:
    cards_html = ""

    for stat in stats:
        cards_html += metric_card_html(
            label=stat["label"],
            value=stat["value"],
            subtitle=stat.get("subtitle"),
        )

    return dedent(
f"""
<div class="profile-metric-grid" style="grid-template-columns: repeat({columns}, minmax(0, 1fr));">
{cards_html}
</div>
"""
    ).strip()


def tab_panel_html(
    title: str,
    description: str,
    stats: list[dict],
    columns: int = 4,
) -> str:
    return dedent(
f"""
<div class="player-tab-panel">
<div class="player-tab-title">{escape(title)}</div>
<div class="player-tab-description">{escape(description)}</div>

{metric_grid_html(stats=stats, columns=columns)}
</div>
"""
    ).strip()


# =============================================================================
# Generic circular rate / donut HTML helpers
# =============================================================================

def circular_rate_html(label: str, value) -> str:
    try:
        numeric_value = 0 if value is None or pd.isna(value) else float(value)
    except (TypeError, ValueError):
        numeric_value = 0

    numeric_value = max(0, min(numeric_value, 100))

    return dedent(
f"""
<div class="circle-rate-card">
<div class="circle-rate-title">{escape(str(label))}</div>

<div class="circle-rate" style="--value: {numeric_value};">
<div class="circle-rate-inner">
<div class="circle-rate-value">{numeric_value:.1f}%</div>
<div class="circle-rate-label">Success rate</div>
</div>
</div>
</div>
"""
    ).strip()


# =============================================================================
# Attack tab HTML helpers
# =============================================================================

def attack_bar_row_html(label: str, value, max_value: float) -> str:
    numeric_value = 0 if value is None or pd.isna(value) else float(value)
    width = 0 if max_value <= 0 else max(0, min((numeric_value / max_value) * 100, 100))

    return dedent(
f"""
<div class="attack-bar-row">
<div class="attack-bar-label">{escape(str(label))}</div>
<div class="attack-bar-track">
<div class="attack-bar-fill" style="width: {width}%;"></div>
</div>
<div class="attack-bar-value">{format_number(numeric_value)}</div>
</div>
"""
    ).strip()


def attack_efficiency_card_html(label: str, value: str) -> str:
    return dedent(
f"""
<div class="attack-efficiency-card">
<div class="attack-efficiency-value">{escape(str(value))}</div>
<div class="attack-efficiency-label">{escape(str(label))}</div>
</div>
"""
    ).strip()


def attack_detail_card_html(label: str, value: str) -> str:
    return dedent(
        f"""
        <div class="attack-detail-card">
            <div class="attack-detail-value">{escape(str(value))}</div>
            <div class="attack-detail-label">{escape(str(label))}</div>
        </div>
        """
    ).strip()


# =============================================================================
# Distribution tab HTML helpers
# =============================================================================

def distribution_feature_row_html(label: str, value: str) -> str:
    return dedent(
        f"""
        <div class="distribution-feature-row">
            <div class="distribution-feature-label">{escape(str(label))}</div>
            <div class="distribution-feature-value">{escape(str(value))}</div>
        </div>
        """
    ).strip()


def distribution_rate_row_html(label: str, value, max_value: float = 100.0) -> str:
    if value is None or pd.isna(value):
        display_value = "-"
        width = 0
    else:
        try:
            numeric_value = float(value)
            display_value = f"{numeric_value:.1f}%"
            width = max(0, min((numeric_value / max_value) * 100, 100))
        except (TypeError, ValueError):
            display_value = "-"
            width = 0

    return dedent(
        f"""
        <div class="distribution-rate-row">
            <div class="distribution-rate-header">
                <span>{escape(str(label))}</span>
                <strong>{escape(display_value)}</strong>
            </div>
            <div class="distribution-rate-track">
                <div class="distribution-rate-fill" style="width: {width}%;"></div>
            </div>
        </div>
        """
    ).strip()


def distribution_detail_card_html(label: str, value: str) -> str:
    return dedent(
        f"""
        <div class="distribution-detail-card">
            <div class="distribution-detail-value">{escape(str(value))}</div>
            <div class="distribution-detail-label">{escape(str(label))}</div>
        </div>
        """
    ).strip()


# =============================================================================
# Defence tab HTML helpers
# =============================================================================

def defence_feature_row_html(label: str, value: str) -> str:
    return dedent(
        f"""
        <div class="defence-feature-row">
            <div class="defence-feature-label">{escape(str(label))}</div>
            <div class="defence-feature-value">{escape(str(value))}</div>
        </div>
        """
    ).strip()


def defence_rate_row_html(label: str, value, max_value: float = 100.0) -> str:
    if value is None or pd.isna(value):
        display_value = "-"
        width = 0
    else:
        try:
            numeric_value = float(value)
            display_value = f"{numeric_value:.1f}%"
            width = max(0, min((numeric_value / max_value) * 100, 100))
        except (TypeError, ValueError):
            display_value = "-"
            width = 0

    return dedent(
        f"""
        <div class="defence-rate-row">
            <div class="defence-rate-header">
                <span>{escape(str(label))}</span>
                <strong>{escape(display_value)}</strong>
            </div>
            <div class="defence-rate-track">
                <div class="defence-rate-fill" style="width: {width}%;"></div>
            </div>
        </div>
        """
    ).strip()


def defence_detail_card_html(label: str, value: str) -> str:
    return dedent(
        f"""
        <div class="defence-detail-card">
            <div class="defence-detail-value">{escape(str(value))}</div>
            <div class="defence-detail-label">{escape(str(label))}</div>
        </div>
        """
    ).strip()
    
# =============================================================================
# Goalkeeping tab HTML helpers
# =============================================================================

def goalkeeping_detail_card_html(label: str, value: str) -> str:
    return dedent(
        f"""
        <div class="goalkeeping-detail-card">
            <div class="goalkeeping-detail-value">{escape(str(value))}</div>
            <div class="goalkeeping-detail-label">{escape(str(label))}</div>
        </div>
        """
    ).strip()


def goalkeeping_secondary_card_html(label: str, value: str) -> str:
    return dedent(
        f"""
        <div class="goalkeeping-secondary-card">
            <div class="goalkeeping-secondary-value">{escape(str(value))}</div>
            <div class="goalkeeping-secondary-label">{escape(str(label))}</div>
        </div>
        """
    ).strip()