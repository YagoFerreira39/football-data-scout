# =========================
# TEAM STYLE CONFIG
# =========================

TEAM_STYLE_PROFILE_CONFIG = {
    "possession_control": {
        "label": "Possession Control",
        "higher_is_better": [
            "Possession Percentage",
            "passes_per_game",
            "open_play_passes_per_game",
            "pass_accuracy_pct",
        ],
        "lower_is_better": [],
    },

    "territory_penetration": {
        "label": "Territory & Penetration",
        "higher_is_better": [
            "final_third_touches_per_game",
            "successful_passes_opp_half_per_game",
            "key_passes_per_game",
            "shots_created_per_game",
        ],
        "lower_is_better": [],
    },

    "attacking_volume": {
        "label": "Attacking Volume",
        "higher_is_better": [
            "shots_per_game",
            "shots_on_target_per_game",
            "goals_per_game",
            "goal_conversion_pct",
        ],
        "lower_is_better": [],
    },

    "pressing_ball_winning": {
        "label": "Pressing & Ball Winning",
        "higher_is_better": [
            "defensive_actions_per_game",
            "recoveries_per_game",
            "interceptions_per_game",
        ],
        "lower_is_better": [
            "PPDA",
        ],
    },

    "defensive_resistance": {
        "label": "Defensive Resistance",
        "higher_is_better": [
            "clean_sheet_rate_pct",
            "duels_won_pct",
        ],
        "lower_is_better": [
            "goals_conceded_per_game",
            "shots_conceded_per_game",
        ],
    },

    "directness": {
        "label": "Directness",
        "higher_is_better": [
            "long_passes_per_game",
            "launches_per_game",
            "long_pass_share_pct",
        ],
        "lower_is_better": [
            "Possession Percentage",
        ],
    },

    "width_crossing": {
        "label": "Width & Crossing",
        "higher_is_better": [
            "open_play_crosses_per_game",
            "open_play_cross_accuracy_pct",
            "cross_share_pct",
            "corners_taken_per_game",
        ],
        "lower_is_better": [],
    },

    "physicality_duels": {
        "label": "Physicality / Duels",
        "higher_is_better": [
            "duels_per_game",
            "aerial_duels_per_game",
            "ground_duels_per_game",
            "duels_won_pct",
            "aerial_duels_won_pct",
            "ground_duels_won_pct",
        ],
        "lower_is_better": [],
    },

    "set_piece_threat": {
        "label": "Set-Piece Threat",
        "higher_is_better": [
            "set_piece_goals_per_game",
            "corners_taken_per_game",
        ],
        "lower_is_better": [],
    },
}


TEAM_STYLE_SCORE_COLUMNS = [
    "possession_control_score",
    "territory_penetration_score",
    "attacking_volume_score",
    "pressing_ball_winning_score",
    "defensive_resistance_score",
    "directness_score",
    "width_crossing_score",
    "physicality_duels_score",
    "set_piece_threat_score",
    "overall_style_intensity_score",
]


TEAM_STYLE_SCORE_LABELS = {
    "possession_control_score": "Possession Control",
    "territory_penetration_score": "Territory & Penetration",
    "attacking_volume_score": "Attacking Volume",
    "pressing_ball_winning_score": "Pressing & Ball Winning",
    "defensive_resistance_score": "Defensive Resistance",
    "directness_score": "Directness",
    "width_crossing_score": "Width & Crossing",
    "physicality_duels_score": "Physicality / Duels",
    "set_piece_threat_score": "Set-Piece Threat",
    "overall_style_intensity_score": "Overall Style Intensity",
}