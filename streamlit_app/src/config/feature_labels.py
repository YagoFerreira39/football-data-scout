# =================
# FEATURE LABELS
# =================
# Human-readable labels shown around the pizza chart
# FEATURE_LABELS = {
#     # =================
#     # General / Metadata
#     # =================
#     "matches_played": "Matches",
#     "minutes_played": "Minutes",
#     "age": "Age",
#     "height": "Height",
#     "weight": "Weight",
#     "market_value": "Market Value",

#     # =================
#     # Shooting / Box Threat
#     # =================
#     "goals": "Goals",
#     "goals_per_90": "Goals/90",
#     "xg": "xG",
#     "xg_per_90": "xG/90",
#     "shots": "Shots",
#     "shots_per_90": "Shots Volume",
#     "shots_on_target_%": "Shot Accuracy",
#     "goal_conversion_%": "Shot Conversion",
#     "non-penalty_goals": "nP Goals",
#     "non-penalty_goals_per_90": "nP Goals/90",
#     "non_penalty_xg": "nP xG",
#     "non_penalty_xg_per_90": "nP xG/90",
#     "touches_in_box_per_90": "Box Touches",
#     "head_goals": "Head Goals",
#     "head_goals_per_90": "Head Goals/90",
#     "penalties_taken": "Penalties Taken",
#     "penalty_conversion_%": "Penalty Conversion",

#     # =================
#     # Creativity / Chance Creation
#     # =================
#     "assists": "Assists",
#     "assists_per_90": "Assists/90",
#     "xa": "xA",
#     "xa_per_90": "xA/90",
#     "xa_per_100_passes": "xA/100 Passes",
#     "shot_assists_per_90": "Shot Assists",
#     "key_passes_per_90": "Key Passes",
#     "key_passes_per_100_passes": "Key Passes/100 Passes",
#     "smart_passes_per_90": "Smart Passes",
#     "accurate_smart_passes_%": "Smart Pass Accuracy",
#     "through_passes_per_90": "Through Passes",
#     "accurate_through_passes_%": "Through Pass Accuracy",
#     "second_assists_per_90": "Second Assists",
#     "third_assists_per_90": "Third Assists",

#     # =================
#     # General Passing / Distribution
#     # =================
#     "passes_per_90": "Passing Volume",
#     "accurate_passes_%": "Pass Accuracy",
#     "forward_passes_per_90": "Forward Passes",
#     "accurate_forward_passes_%": "Forward Pass Accuracy",
#     "back_passes_per_90": "Back Passes",
#     "accurate_back_passes_%": "Back Pass Accuracy",
#     "lateral_passes_per_90": "Lateral Passes",
#     "accurate_lateral_passes_%": "Lateral Pass Accuracy",
#     "short_/_medium_passes_per_90": "Short/Medium Passes",
#     "accurate_short_/_medium_passes_%": "Short/Medium Pass Accuracy",
#     "received_passes_per_90": "Ball Reception",
#     "received_long_passes_per_90": "Long Ball Reception",
#     "average_pass_length_m": "Avg Pass Length",

#     # =================
#     # Progression / Penetration
#     # =================
#     "progressive_passes_per_90": "Progressive Passes",
#     "accurate_progressive_passes_%": "Progressive Pass Accuracy",
#     "progressive_runs_per_90": "Progressive Runs",
#     "passes_to_final_third_per_90": "Final 3rd Passes",
#     "accurate_passes_to_final_third_%": "Final 3rd Pass Accuracy",
#     "passes_to_penalty_area_per_90": "Penalty Area Passes",
#     "accurate_passes_to_penalty_area_%": "Penalty Area Pass Accuracy",
#     "deep_completions_per_90": "Deep Completions",

#     # =================
#     # Long Passing
#     # =================
#     "long_passes_per_90": "Long Passes",
#     "accurate_long_passes_%": "Long Pass Accuracy",
#     "average_long_pass_length_m": "Long Pass Length",

#     # =================
#     # Crossing / Delivery
#     # =================
#     "crosses_per_90": "Crosses",
#     "accurate_crosses_%": "Cross Accuracy",
#     "crosses_from_left_flank_per_90": "Left Flank Crosses",
#     "accurate_crosses_from_left_flank_%": "Left Cross Accuracy",
#     "crosses_from_right_flank_per_90": "Right Flank Crosses",
#     "accurate_crosses_from_right_flank_%": "Right Cross Accuracy",
#     "crosses_to_goalie_box_per_90": "Goal Box Crosses",
#     "deep_completed_crosses_per_90": "Deep Crosses",

#     # =================
#     # Dribbling / 1v1 Ability
#     # =================
#     "dribbles_per_90": "Dribbles",
#     "successful_dribbles_%": "Dribble Success",
#     "offensive_duels_per_90": "Off. Duels",
#     "offensive_duels_won_%": "Off. Duel Win %",
#     "successful_attacking_actions_per_90": "Successful Att. Actions",
#     "fouls_suffered_per_90": "Fouls Suffered",
#     "accelerations_per_90": "Accelerations",

#     # =================
#     # Duels / Physical Contest
#     # =================
#     "duels_per_90": "Total Duels",
#     "duels_won_%": "Total Duel Win %",

#     # =================
#     # Defending / Discipline
#     # =================
#     "successful_defensive_actions_per_90": "Defensive Actions",
#     "defensive_duels_per_90": "Defensive Duels",
#     "defensive_duels_won_%": "Def. Duel Win %",
#     "interceptions_per_90": "Interceptions",
#     "padj_interceptions": "Adj. Interceptions",
#     "p_adj_interceptions": "Adj. Interceptions",
#     "shots_blocked_per_90": "Shots Blocked",
#     "sliding_tackles_per_90": "Sliding Tackles",
#     "padj_sliding_tackles": "Adj. Sliding Tackles",
#     "p_adj_sliding_tackles": "Adj. Sliding Tackles",
#     "fouls_per_90": "Fouls Committed",
#     "yellow_cards": "Yellow Cards",
#     "yellow_cards_per_90": "Yellow Cards/90",
#     "red_cards": "Red Cards",
#     "red_cards_per_90": "Red Cards/90",

#     # =================
#     # Aerial Ability
#     # =================
#     "aerial_duels_per_90": "Aerial Duels",
#     "aerial_duels_won_%": "Aerial Win %",

#     # =================
#     # Set Pieces
#     # =================
#     "free_kicks_per_90": "Free Kicks",
#     "direct_free_kicks_per_90": "Direct Free Kicks",
#     "direct_free_kicks_on_target_%": "Direct FK Accuracy",
#     "corners_per_90": "Corners",

#     # =================
#     # Goalkeeper
#     # =================
#     "conceded_goals": "Goals Conceded",
#     "conceded_goals_per_90": "Goals Conceded/90",
#     "shots_against": "Shots Against",
#     "shots_against_per_90": "Shots Against/90",
#     "clean_sheets": "Clean Sheets",
#     "save_rate_%": "Save Rate",
#     "xg_against": "xG Against",
#     "xg_against_per_90": "xG Against/90",
#     "prevented_goals": "Prevented Goals",
#     "prevented_goals_per_90": "Prevented Goals/90",
#     "back_passes_received_as_gk_per_90": "GK Back Passes Received",
#     "exits_per_90": "Exits",
#     "aerial_duels_per_90.1": "GK Aerial Duels",
#     "aerial_duels_per_90_1": "GK Aerial Duels",
# }

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