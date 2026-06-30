# =========================
# PLAY STYLE PROFILE CONFIG
# =========================

PLAY_STYLE_SCORE_PREFIX = "play_style"


PLAY_STYLE_DIMENSIONS = {
    "defence": {
        "label": "Defence",
        "left_label": "Low block",
        "right_label": "High press",
        "right_indicators": [
            {"column": "defensive_actions_per_game", "weight": 0.35},
            {"column": "recoveries_per_game", "weight": 0.25},
            {"column": "interceptions_per_game", "weight": 0.15},
        ],
        "left_indicators": [
            {"column": "PPDA", "weight": 0.25},
        ],
    },

    "defensive_transition": {
        "label": "Defensive Transition",
        "left_label": "Fall back",
        "right_label": "Counter press",
        "right_indicators": [
            {"column": "recoveries_per_game", "weight": 0.35},
            {"column": "interceptions_per_game", "weight": 0.25},
            {"column": "defensive_actions_per_game", "weight": 0.25},
        ],
        "left_indicators": [
            {"column": "PPDA", "weight": 0.15},
        ],
    },

    "attack": {
        "label": "Attack",
        "left_label": "Long ball",
        "right_label": "Build-up",
        "right_indicators": [
            {"column": "Possession Percentage", "weight": 0.25},
            {"column": "passes_per_game", "weight": 0.25},
            {"column": "open_play_passes_per_game", "weight": 0.20},
            {"column": "pass_accuracy_pct", "weight": 0.15},
        ],
        "left_indicators": [
            {"column": "long_pass_share_pct", "weight": 0.10},
            {"column": "launches_per_game", "weight": 0.05},
        ],
    },

    "penetration": {
        "label": "Penetration",
        "left_label": "Crossing",
        "right_label": "Combination play",
        "right_indicators": [
            {"column": "key_passes_per_game", "weight": 0.30},
            {"column": "shots_created_per_game", "weight": 0.25},
            {"column": "successful_passes_opp_half_per_game", "weight": 0.20},
            {"column": "final_third_touches_per_game", "weight": 0.15},
        ],
        "left_indicators": [
            {"column": "open_play_crosses_per_game", "weight": 0.05},
            {"column": "cross_share_pct", "weight": 0.05},
        ],
    },

    "chance_creation": {
        "label": "Chance Creation",
        "left_label": "Sustained",
        "right_label": "Direct",
        "right_indicators": [
            {"column": "long_pass_share_pct", "weight": 0.25},
            {"column": "launches_per_game", "weight": 0.20},
            {"column": "shots_per_game", "weight": 0.15},
        ],
        "left_indicators": [
            {"column": "Possession Percentage", "weight": 0.20},
            {"column": "final_third_touches_per_game", "weight": 0.10},
            {"column": "passes_per_game", "weight": 0.10},
        ],
    },

    "outcome": {
        "label": "Outcome",
        "left_label": "Poor",
        "right_label": "Great",
        "right_indicators": [
            {"column": "goal_difference_per_game", "weight": 0.35},
            {"column": "goals_per_game", "weight": 0.25},
            {"column": "clean_sheet_rate_pct", "weight": 0.15},
            {"column": "shots_on_target_pct", "weight": 0.10},
        ],
        "left_indicators": [
            {"column": "goals_conceded_per_game", "weight": 0.10},
            {"column": "shots_conceded_per_game", "weight": 0.05},
        ],
    },
}