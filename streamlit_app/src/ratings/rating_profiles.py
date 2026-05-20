# =============================================================================
# Rating profile positions
# =============================================================================

CB_POSITIONS = ["CB", "RCB", "LCB"]
FB_WB_POSITIONS = ["RB", "LB", "RWB", "LWB"]
MF_POSITIONS = ["DMF", "RDMF", "LDMF", "CMF", "RCMF", "LCMF"]
AM_POSITIONS = ["AMF"]
WINGER_POSITIONS = ["RW", "LW", "RAMF", "LAMF", "WF", "RWF", "LWF"]
CF_POSITIONS = ["CF"]


# =============================================================================
# Centre Back - Aerially Dominant
# =============================================================================

CB_AERIALLY_DOMINANT_CATEGORY_WEIGHTS = {
    "Aerial Dominance": 0.40,
    "Defending": 0.35,
    "Ball Retention": 0.15,
    "Progression": 0.10,
}

CB_AERIALLY_DOMINANT_FEATURE_WEIGHTS = {
    "Defending": {
        "defensive_duels_won_%": 0.35,
        "defensive_duels_per_90": 0.30,
        "shots_blocked_per_90": 0.20,
        "interceptions_per_90": 0.15,
    },
    "Aerial Dominance": {
        "aerial_duels_per_90": 0.40,
        "aerial_duels_won_%": 0.55,
        "head_goals_per_90": 0.05,
    },
    "Ball Retention": {
        "passes_per_90": 0.20,
        "accurate_passes_%": 0.35,
        "forward_passes_per_90": 0.20,
        "accurate_forward_passes_%": 0.25,
    },
    "Progression": {
        "progressive_passes_per_90": 0.30,
        "passes_to_final_third_per_90": 0.25,
        "long_passes_per_90": 0.20,
        "accurate_long_passes_%": 0.25,
    },
}


# =============================================================================
# Centre Back - Ball Playing
# =============================================================================

CB_BALL_PLAYING_CATEGORY_WEIGHTS = {
    "Passing Progression": 0.30,
    "Defending": 0.20,
    "Ball Carrying": 0.15,
    "Ball Retention": 0.15,
    "Long Distribution": 0.10,
    "Aerial Ability": 0.10,
}

CB_BALL_PLAYING_FEATURE_WEIGHTS = {
    "Passing Progression": {
        "progressive_passes_per_90": 0.35,
        "accurate_progressive_passes_%": 0.25,
        "passes_to_final_third_per_90": 0.25,
        "accurate_passes_to_final_third_%": 0.15,
    },
    "Defending": {
        "defensive_duels_won_%": 0.35,
        "defensive_duels_per_90": 0.25,
        "padj_interceptions": 0.20,
        "padj_sliding_tackles": 0.20,
    },
    "Ball Carrying": {
        "progressive_runs_per_90": 0.70,
        "accelerations_per_90": 0.30,
    },
    "Ball Retention": {
        "accurate_passes_%": 0.35,
        "accurate_short_/_medium_passes_%": 0.35,
        "short_/_medium_passes_per_90": 0.20,
        "fouls_suffered_per_90": 0.10,
    },
    "Long Distribution": {
        "accurate_long_passes_%": 0.30,
        "long_passes_per_90": 0.25,
        "accurate_forward_passes_%": 0.25,
        "forward_passes_per_90": 0.20,
    },
    "Aerial Ability": {
        "aerial_duels_won_%": 0.55,
        "aerial_duels_per_90": 0.45,
    },
}


# =============================================================================
# Fullback - Defensive
# =============================================================================

DEFENSIVE_FULL_BACK_CATEGORY_WEIGHTS = {
    "Defending": 0.40,
    "Ball Retention": 0.30,
    "Aerial Ability": 0.20,
    "Passing Progression": 0.10,
}

DEFENSIVE_FULL_BACK_FEATURE_WEIGHTS = {
    "Defending": {
        "padj_interceptions": 0.20,
        "padj_sliding_tackles": 0.20,
        "defensive_duels_per_90": 0.25,
        "defensive_duels_won_%": 0.35,
    },
    "Ball Retention": {
        "accurate_passes_%": 0.40,
        "accurate_short_/_medium_passes_%": 0.35,
        "passes_per_90": 0.25,
    },
    "Aerial Ability": {
        "aerial_duels_won_%": 0.55,
        "aerial_duels_per_90": 0.45,
    },
    "Passing Progression": {
        "forward_passes_per_90": 0.45,
        "accurate_forward_passes_%": 0.55,
    },
}


# =============================================================================
# Fullback - Attacking
# =============================================================================

ATTACKING_FULL_BACK_CATEGORY_WEIGHTS = {
    "Crossing": 0.25,
    "Dribbling": 0.25,
    "Chance Creation": 0.20,
    "Defending": 0.15,
    "Progression": 0.10,
    "Aerial Ability": 0.05,
}

ATTACKING_FULL_BACK_FEATURE_WEIGHTS = {
    "Crossing": {
        "accurate_crosses_%": 0.60,
        "crosses_per_90": 0.40,
    },
    "Dribbling": {
        "dribbles_per_90": 0.60,
        "successful_dribbles_%": 0.40,
    },
    "Chance Creation": {
        "xa_per_90": 0.50,
        "key_passes_per_90": 0.30,
        "assists_per_90": 0.20,
    },
    "Defending": {
        "defensive_duels_won_%": 0.55,
        "defensive_duels_per_90": 0.35,
        "padj_interceptions": 0.10,
    },
    "Progression": {
        "progressive_runs_per_90": 0.30,
        "progressive_passes_per_90": 0.30,
        "accurate_progressive_passes_%": 0.25,
        "accurate_passes_to_final_third_%": 0.15,
    },
    "Aerial Ability": {
        "aerial_duels_per_90": 0.35,
        "aerial_duels_won_%": 0.65,
    },
}


# =============================================================================
# Fullback - Inverted
# =============================================================================

INVERTED_FULL_BACK_CATEGORY_WEIGHTS = {
    "Involvement": 0.35,
    "Passing Progression": 0.25,
    "Ball Retention": 0.20,
    "Defending": 0.20,
}

INVERTED_FULL_BACK_FEATURE_WEIGHTS = {
    "Involvement": {
        "received_passes_per_90": 0.40,
        "passes_per_90": 0.35,
        "short_/_medium_passes_per_90": 0.25,
    },
    "Passing Progression": {
        "progressive_passes_per_90": 0.40,
        "accurate_progressive_passes_%": 0.30,
        "passes_to_final_third_per_90": 0.30,
    },
    "Ball Retention": {
        "accurate_passes_%": 0.40,
        "accurate_short_/_medium_passes_%": 0.40,
        "fouls_suffered_per_90": 0.20,
    },
    "Defending": {
        "padj_interceptions": 0.35,
        "defensive_duels_per_90": 0.30,
        "defensive_duels_won_%": 0.35,
    },
}


# =============================================================================
# Wing Back
# =============================================================================

WING_BACK_CATEGORY_WEIGHTS = {
    "Crossing": 0.25,
    "Chance Creation": 0.25,
    "Progression": 0.15,
    "Dribbling": 0.10,
    "Attacking Threat": 0.10,
    "Defensive Duels": 0.08,
    "Proactive Defending": 0.07,
}

WING_BACK_FEATURE_WEIGHTS = {
    "Crossing": {
        "accurate_crosses_%": 0.55,
        "crosses_per_90": 0.45,
    },
    "Chance Creation": {
        "xa_per_90": 0.40,
        "key_passes_per_90": 0.30,
        "accurate_passes_to_penalty_area_%": 0.20,
        "assists_per_90": 0.10,
    },
    "Progression": {
        "progressive_runs_per_90": 0.40,
        "progressive_passes_per_90": 0.30,
        "passes_to_final_third_per_90": 0.30,
    },
    "Dribbling": {
        "dribbles_per_90": 0.35,
        "successful_dribbles_%": 0.35,
        "offensive_duels_won_%": 0.30,
    },
    "Attacking Threat": {
        "non_penalty_xg_per_90": 0.40,
        "shots_on_target_%": 0.35,
        "touches_in_box_per_90": 0.25,
    },
    "Defensive Duels": {
        "defensive_duels_won_%": 0.40,
        "defensive_duels_per_90": 0.30,
        "aerial_duels_won_%": 0.20,
        "aerial_duels_per_90": 0.10,
    },
    "Proactive Defending": {
        "interceptions_per_90": 0.40,
        "padj_interceptions": 0.35,
        "padj_sliding_tackles": 0.25,
    },
}


# =============================================================================
# Defensive Midfielder / Central Midfielder - Ball Playing
# =============================================================================

DM_BALL_PLAYING_CATEGORY_WEIGHTS = {
    "Distribution": 0.25,
    "Progression": 0.25,
    "Defending": 0.20,
    "Press Resistance": 0.10,
    "Ball Carrying": 0.10,
    "Long Distribution": 0.10,
}

DM_BALL_PLAYING_FEATURE_WEIGHTS = {
    "Distribution": {
        "passes_per_90": 0.40,
        "accurate_passes_%": 0.30,
        "short_/_medium_passes_per_90": 0.20,
        "accurate_short_/_medium_passes_%": 0.10,
    },
    "Progression": {
        "progressive_passes_per_90": 0.35,
        "accurate_progressive_passes_%": 0.25,
        "passes_to_final_third_per_90": 0.25,
        "accurate_passes_to_final_third_%": 0.15,
    },
    "Defending": {
        "padj_interceptions": 0.30,
        "padj_sliding_tackles": 0.30,
        "defensive_duels_per_90": 0.20,
        "defensive_duels_won_%": 0.20,
    },
    "Press Resistance": {
        "received_passes_per_90": 0.60,
        "fouls_suffered_per_90": 0.40,
    },
    "Ball Carrying": {
        "dribbles_per_90": 0.40,
        "successful_dribbles_%": 0.35,
        "progressive_runs_per_90": 0.25,
    },
    "Long Distribution": {
        "long_passes_per_90": 0.35,
        "accurate_long_passes_%": 0.35,
        "forward_passes_per_90": 0.15,
        "accurate_forward_passes_%": 0.15,
    },
}


# =============================================================================
# Defensive Midfielder / Central Midfielder - Ball Winning
# =============================================================================

DM_BALL_WINNING_CATEGORY_WEIGHTS = {
    "Defending": 0.35,
    "Duel Winning": 0.25,
    "Ball Retention": 0.20,
    "Forward Release": 0.20,
}

DM_BALL_WINNING_FEATURE_WEIGHTS = {
    "Defending": {
        "padj_interceptions": 0.45,
        "interceptions_per_90": 0.20,
        "successful_defensive_actions_per_90": 0.20,
        "shots_blocked_per_90": 0.15,
    },
    "Duel Winning": {
        "defensive_duels_per_90": 0.30,
        "defensive_duels_won_%": 0.30,
        "padj_sliding_tackles": 0.15,
        "aerial_duels_per_90": 0.10,
        "aerial_duels_won_%": 0.15,
    },
    "Ball Retention": {
        "passes_per_90": 0.25,
        "accurate_passes_%": 0.30,
        "short_/_medium_passes_per_90": 0.25,
        "accurate_short_/_medium_passes_%": 0.20,
    },
    "Forward Release": {
        "forward_passes_per_90": 0.20,
        "accurate_forward_passes_%": 0.20,
        "progressive_passes_per_90": 0.20,
        "accurate_progressive_passes_%": 0.15,
        "long_passes_per_90": 0.15,
        "accurate_long_passes_%": 0.10,
    },
}


# =============================================================================
# Central Midfielder - Box to Box
# =============================================================================

CM_BOX_TO_BOX_CATEGORY_WEIGHTS = {
    "Defending": 0.25,
    "Box Threat": 0.20,
    "Ball Carrying": 0.20,
    "Passing Progression": 0.15,
    "Ball Retention": 0.10,
    "Chance Creation": 0.10,
}

CM_BOX_TO_BOX_FEATURE_WEIGHTS = {
    "Defending": {
        "defensive_duels_per_90": 0.30,
        "defensive_duels_won_%": 0.30,
        "padj_interceptions": 0.20,
        "padj_sliding_tackles": 0.20,
    },
    "Box Threat": {
        "touches_in_box_per_90": 0.35,
        "non_penalty_xg_per_90": 0.30,
        "shots_per_90": 0.25,
        "non-penalty_goals_per_90": 0.10,
    },
    "Ball Carrying": {
        "progressive_runs_per_90": 0.45,
        "accelerations_per_90": 0.30,
        "received_passes_per_90": 0.25,
    },
    "Passing Progression": {
        "progressive_passes_per_90": 0.35,
        "passes_to_final_third_per_90": 0.25,
        "accurate_progressive_passes_%": 0.20,
        "accurate_passes_to_final_third_%": 0.20,
    },
    "Ball Retention": {
        "passes_per_90": 0.40,
        "accurate_passes_%": 0.60,
    },
    "Chance Creation": {
        "xa_per_90": 0.45,
        "key_passes_per_90": 0.45,
        "shot_assists_per_90": 0.10,
    },
}


# =============================================================================
# Attacking Midfielder
# =============================================================================

AM_CATEGORY_WEIGHTS = {
    "Chance Creation": 0.35,
    "Goal Threat": 0.25,
    "Receiving": 0.20,
    "Passing": 0.10,
    "Dribbling": 0.10,
}

AM_FEATURE_WEIGHTS = {
    "Chance Creation": {
        "xa_per_100_passes": 0.45,
        "key_passes_per_100_passes": 0.40,
        "smart_passes_per_90": 0.10,
    },
    "Goal Threat": {
        "non_penalty_xg_per_90": 0.35,
        "shots_per_90": 0.25,
        "non-penalty_goals_per_90": 0.20,
        "shots_on_target_%": 0.20,
    },
    "Receiving": {
        "received_passes_per_90": 0.45,
        "fouls_suffered_per_90": 0.30,
        "touches_in_box_per_90": 0.25,
    },
    "Passing": {
        "passes_per_90": 0.25,
        "accurate_passes_%": 0.25,
        "short_/_medium_passes_per_90": 0.20,
        "through_passes_per_90": 0.30,
    },
    "Dribbling": {
        "dribbles_per_90": 0.55,
        "successful_dribbles_%": 0.45,
    },
}


# =============================================================================
# Winger - Touchline
# =============================================================================

W_TOUCHLINE_CATEGORY_WEIGHTS = {
    "Dribbling": 0.30,
    "Crossing": 0.25,
    "Chance Creation": 0.25,
    "Ball Retention": 0.15,
    "Progression": 0.05,
    "Defensive Contribution": 0.05,
}

W_TOUCHLINE_FEATURE_WEIGHTS = {
    "Dribbling": {
        "dribbles_per_90": 0.35,
        "successful_dribbles_%": 0.40,
        "offensive_duels_won_%": 0.15,
        "offensive_duels_per_90": 0.10,
    },
    "Crossing": {
        "accurate_crosses_%": 0.45,
        "crosses_per_90": 0.35,
        "deep_completed_crosses_per_90": 0.20,
    },
    "Chance Creation": {
        "xa_per_90": 0.40,
        "key_passes_per_90": 0.35,
        "passes_to_penalty_area_per_90": 0.10,
        "accurate_passes_to_penalty_area_%": 0.15,
    },
    "Ball Retention": {
        "received_passes_per_90": 0.40,
        "accurate_short_/_medium_passes_%": 0.30,
        "accurate_passes_%": 0.30,
    },
    "Progression": {
        "progressive_runs_per_90": 0.40,
        "accelerations_per_90": 0.20,
        "progressive_passes_per_90": 0.20,
        "passes_to_final_third_per_90": 0.20,
    },
    "Defensive Contribution": {
        "defensive_duels_per_90": 0.60,
        "defensive_duels_won_%": 0.40,
    },
}


# =============================================================================
# Winger - Half-Space Drifter
# =============================================================================

W_HALF_SPACE_DRIFTER_CATEGORY_WEIGHTS = {
    "Chance Creation": 0.30,
    "Goal Threat": 0.20,
    "Dribbling": 0.20,
    "Passing": 0.20,
    "Passing Progression": 0.05,
    "Crossing": 0.05,
}

W_HALF_SPACE_DRIFTER_FEATURE_WEIGHTS = {
    "Chance Creation": {
        "xa_per_90": 0.50,
        "key_passes_per_90": 0.35,
        "smart_passes_per_90": 0.15,
    },
    "Goal Threat": {
        "non_penalty_xg_per_90": 0.35,
        "shots_per_90": 0.25,
        "touches_in_box_per_90": 0.25,
        "shots_on_target_%": 0.15,
    },
    "Dribbling": {
        "dribbles_per_90": 0.35,
        "successful_dribbles_%": 0.45,
        "accelerations_per_90": 0.15,
        "progressive_runs_per_90": 0.05,
    },
    "Passing": {
        "passes_per_90": 0.35,
        "accurate_passes_%": 0.35,
        "short_/_medium_passes_per_90": 0.15,
        "accurate_short_/_medium_passes_%": 0.15,
    },
    "Passing Progression": {
        "progressive_passes_per_90": 0.35,
        "passes_to_final_third_per_90": 0.30,
        "through_passes_per_90": 0.20,
        "accurate_progressive_passes_%": 0.15,
    },
    "Crossing": {
        "crosses_per_90": 0.40,
        "accurate_crosses_%": 0.60,
    },
}


# =============================================================================
# Winger - Inside Forward
# =============================================================================

W_INSIDE_FORWARD_CATEGORY_WEIGHTS = {
    "Box Threat": 0.35,
    "Final Third Output": 0.25,
    "Ball Carrying": 0.20,
    "Attacking Involvement": 0.20,
}

W_INSIDE_FORWARD_FEATURE_WEIGHTS = {
    "Box Threat": {
        "non_penalty_xg_per_90": 0.40,
        "non-penalty_goals_per_90": 0.25,
        "touches_in_box_per_90": 0.25,
        "received_passes_per_90": 0.10,
    },
    "Final Third Output": {
        "shots_per_90": 0.35,
        "shots_on_target_%": 0.25,
        "goal_conversion_%": 0.15,
        "xa_per_90": 0.15,
        "key_passes_per_90": 0.10,
    },
    "Ball Carrying": {
        "progressive_runs_per_90": 0.35,
        "dribbles_per_90": 0.25,
        "successful_dribbles_%": 0.20,
        "offensive_duels_won_%": 0.10,
        "accelerations_per_90": 0.10,
    },
    "Attacking Involvement": {
        "successful_attacking_actions_per_90": 0.40,
        "shot_assists_per_90": 0.40,
        "fouls_suffered_per_90": 0.20,
    },
}


# =============================================================================
# Centre Forward - Mobile / Run Behind
# =============================================================================

CF_MOBILE_RUN_BEHIND_CATEGORY_WEIGHTS = {
    "Box Threat": 0.30,
    "Finishing": 0.30,
    "Depth Threat": 0.25,
    "Ball Carrying": 0.15,
}

CF_MOBILE_RUN_BEHIND_FEATURE_WEIGHTS = {
    "Box Threat": {
        "non_penalty_xg_per_90": 0.45,
        "touches_in_box_per_90": 0.35,
        "shots_per_90": 0.20,
    },
    "Finishing": {
        "non-penalty_goals_per_90": 0.40,
        "shots_on_target_%": 0.35,
        "goal_conversion_%": 0.25,
    },
    "Depth Threat": {
        "received_long_passes_per_90": 0.40,
        "accelerations_per_90": 0.35,
        "received_passes_per_90": 0.25,
    },
    "Ball Carrying": {
        "progressive_runs_per_90": 0.35,
        "dribbles_per_90": 0.25,
        "successful_dribbles_%": 0.25,
        "offensive_duels_won_%": 0.15,
    },
}


# =============================================================================
# Centre Forward - Target Man
# =============================================================================

CF_TARGET_MAN_CATEGORY_WEIGHTS = {    
    "Aerial Dominance": 0.30,
    "Box Threat": 0.45,
    "Reference Play": 0.15,
    "Link-Up Play": 0.10,
}

CF_TARGET_MAN_FEATURE_WEIGHTS = {
    "Reference Play": {
        "received_long_passes_per_90": 0.25,
        "offensive_duels_per_90": 0.35,
        "offensive_duels_won_%": 0.35,
    },
    "Aerial Dominance": {
        "aerial_duels_per_90": 0.45,
        "aerial_duels_won_%": 0.35,
        "head_goals_per_90": 0.20,
    },
    "Box Threat": {
        "non_penalty_xg_per_90": 0.35,
        "non-penalty_goals_per_90": 0.25,
        "shots_per_90": 0.20,
        "shots_on_target_%": 0.20,
    },
    "Link-Up Play": {
        "received_passes_per_90": 0.30,
        "short_/_medium_passes_per_90": 0.25,
        "accurate_short_/_medium_passes_%": 0.25,
        "shot_assists_per_90": 0.20,
    },
}


# =============================================================================
# Rating profile selector options
# =============================================================================

RATING_PROFILE_OPTIONS = {
    "Centre Backs - Aerially Dominant": {
        "positions": CB_POSITIONS,
        "category_weights": CB_AERIALLY_DOMINANT_CATEGORY_WEIGHTS,
        "feature_weights": CB_AERIALLY_DOMINANT_FEATURE_WEIGHTS,
    },
    "Centre Backs - Ball Playing": {
        "positions": CB_POSITIONS,
        "category_weights": CB_BALL_PLAYING_CATEGORY_WEIGHTS,
        "feature_weights": CB_BALL_PLAYING_FEATURE_WEIGHTS,
    },
    "Fullbacks - Defensive": {
        "positions": FB_WB_POSITIONS,
        "category_weights": DEFENSIVE_FULL_BACK_CATEGORY_WEIGHTS,
        "feature_weights": DEFENSIVE_FULL_BACK_FEATURE_WEIGHTS,
    },
    "Fullbacks - Attacking": {
        "positions": FB_WB_POSITIONS,
        "category_weights": ATTACKING_FULL_BACK_CATEGORY_WEIGHTS,
        "feature_weights": ATTACKING_FULL_BACK_FEATURE_WEIGHTS,
    },
    "Fullbacks - Inverted": {
        "positions": FB_WB_POSITIONS,
        "category_weights": INVERTED_FULL_BACK_CATEGORY_WEIGHTS,
        "feature_weights": INVERTED_FULL_BACK_FEATURE_WEIGHTS,
    },
    "Wing Backs": {
        "positions": FB_WB_POSITIONS,
        "category_weights": WING_BACK_CATEGORY_WEIGHTS,
        "feature_weights": WING_BACK_FEATURE_WEIGHTS,
    },
    "Midfielders - Ball Playing": {
        "positions": MF_POSITIONS,
        "category_weights": DM_BALL_PLAYING_CATEGORY_WEIGHTS,
        "feature_weights": DM_BALL_PLAYING_FEATURE_WEIGHTS,
    },
    "Midfielders - Ball Winning": {
        "positions": MF_POSITIONS,
        "category_weights": DM_BALL_WINNING_CATEGORY_WEIGHTS,
        "feature_weights": DM_BALL_WINNING_FEATURE_WEIGHTS,
    },
    "Midfielders - Box to Box": {
        "positions": MF_POSITIONS,
        "category_weights": CM_BOX_TO_BOX_CATEGORY_WEIGHTS,
        "feature_weights": CM_BOX_TO_BOX_FEATURE_WEIGHTS,
    },
    "Attacking Midfielders": {
        "positions": AM_POSITIONS,
        "category_weights": AM_CATEGORY_WEIGHTS,
        "feature_weights": AM_FEATURE_WEIGHTS,
    },
    "Wingers - Touchline": {
        "positions": WINGER_POSITIONS,
        "category_weights": W_TOUCHLINE_CATEGORY_WEIGHTS,
        "feature_weights": W_TOUCHLINE_FEATURE_WEIGHTS,
    },
    "Wingers - Half-Space Drifter": {
        "positions": WINGER_POSITIONS,
        "category_weights": W_HALF_SPACE_DRIFTER_CATEGORY_WEIGHTS,
        "feature_weights": W_HALF_SPACE_DRIFTER_FEATURE_WEIGHTS,
    },
    "Wingers - Inside Forward": {
        "positions": WINGER_POSITIONS,
        "category_weights": W_INSIDE_FORWARD_CATEGORY_WEIGHTS,
        "feature_weights": W_INSIDE_FORWARD_FEATURE_WEIGHTS,
    },
    "Strikers - Mobile / Run Behind": {
        "positions": CF_POSITIONS,
        "category_weights": CF_MOBILE_RUN_BEHIND_CATEGORY_WEIGHTS,
        "feature_weights": CF_MOBILE_RUN_BEHIND_FEATURE_WEIGHTS,
    },
    "Strikers - Target Man": {
        "positions": CF_POSITIONS,
        "category_weights": CF_TARGET_MAN_CATEGORY_WEIGHTS,
        "feature_weights": CF_TARGET_MAN_FEATURE_WEIGHTS,
    },
}