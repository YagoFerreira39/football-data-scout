# =========================
# TEAM PROFILE CONFIG
# =========================

TEAM_PROFILE_ID_COLUMNS = [
    "badge_lg",
    "badge_sm",
    "contestant_name",
    "source_country_name",
    "source_league_name",
    "source_season",
]


TEAM_PROFILE_OVERVIEW_COLUMNS = [
    "Games Played",
    "Goals",
    "Goals Conceded",
    "Clean Sheets",
    "Possession Percentage",
    "PPDA",
]


TEAM_PROFILE_METRIC_GROUPS = {
    "attacking": {
        "label": "Attacking",
        "columns": [
            "goals_per_game",
            "shots_per_game",
            "shots_on_target_per_game",
            "goal_conversion_pct",
            "key_passes_per_game",
            "shots_created_per_game",
            "final_third_touches_per_game",
        ],
    },
    "possession": {
        "label": "Possession / Build-up",
        "columns": [
            "Possession Percentage",
            "passes_per_game",
            "open_play_passes_per_game",
            "pass_accuracy_pct",
        ],
    },
    "defending": {
        "label": "Defending",
        "columns": [
            "goals_conceded_per_game",
            "shots_conceded_per_game",
            "clean_sheet_rate_pct",
            "recoveries_per_game",
            "interceptions_per_game",
            "clearances_per_game",
            "blocks_per_game",
            "PPDA",
        ],
    },
    "duels": {
        "label": "Duels",
        "columns": [
            "duels_per_game",
            "aerial_duels_per_game",
            "ground_duels_per_game",
            "duels_won_pct",
            "aerial_duels_won_pct",
            "ground_duels_won_pct",
        ],
    },
}


LOWER_IS_BETTER_TEAM_METRICS = {
    "goals_conceded_per_game",
    "shots_conceded_per_game",
    "PPDA",
}