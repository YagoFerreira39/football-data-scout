# Wyscout Player Dataset — Column Dictionary

## Player Identity & Context

- **player** — Player full name.  
- **team** — Team the player represents.  
- **team_within_selected_timeframe** — Team during the filtered time period.  
- **position** — Registered tactical position category.  
- **main_position** — Primary natural position.  
- **age** — Player age in years.  
- **birth_country** — Country of birth.  
- **passport_country** — Nationality eligibility.  
- **foot** — Preferred foot.  
- **height** — Player height in centimeters.  
- **weight** — Player weight in kilograms.  
- **on_loan** — Indicates if player is on loan.  

## Contract & Market

- **market_value** — Estimated transfer market value.  
- **contract_expires** — Contract end date.  

## Participation Volume

- **matches_played** — Total matches played.  
- **minutes_played** — Total minutes played.  

## General Offensive Output

- **goals** — Total goals scored.  
- **goals_per_90** — Goals scored per 90 minutes.  
- **non-penalty_goals** — Goals excluding penalties.  
- **non-penalty_goals_per_90** — Non-penalty goals per 90 minutes.  
- **xg** — Expected goals total.  
- **xg_per_90** — Expected goals per 90 minutes.  
- **assists** — Total assists.  
- **assists_per_90** — Assists per 90 minutes.  
- **xa** — Expected assists total.  
- **xa_per_90** — Expected assists per 90 minutes.  

## Shooting & Finishing

- **shots** — Total shots attempted.  
- **shots_per_90** — Shots per 90 minutes.  
- **shots_on_target_%** — Percentage of shots on target.  
- **goal_conversion_%** — Percentage of shots converted into goals.  
- **head_goals** — Goals scored with the head.  
- **head_goals_per_90** — Header goals per 90 minutes.  

## Dribbling & Carrying

- **dribbles_per_90** — Dribble attempts per 90 minutes.  
- **successful_dribbles_%** — Percentage of successful dribbles.  
- **progressive_runs_per_90** — Ball carries advancing play significantly.  
- **accelerations_per_90** — Explosive runs with the ball per 90 minutes.  

## Offensive Duels & Box Presence

- **offensive_duels_per_90** — Attacking duels contested per 90 minutes.  
- **offensive_duels_won_%** — Success rate in attacking duels.  
- **touches_in_box_per_90** — Touches inside opponent penalty area.  
- **fouls_suffered_per_90** — Fouls drawn from opponents.  

## Passing Volume & Accuracy

- **passes_per_90** — Total passes attempted per 90 minutes.  
- **accurate_passes_%** — Overall pass completion rate.  
- **forward_passes_per_90** — Forward passes attempted per 90 minutes.  
- **accurate_forward_passes_%** — Forward pass success rate.  
- **back_passes_per_90** — Backward passes attempted per 90 minutes.  
- **accurate_back_passes_%** — Backward pass success rate.  
- **lateral_passes_per_90** — Sideways passes attempted per 90 minutes.  
- **accurate_lateral_passes_%** — Sideways pass success rate.  
- **short_/_medium_passes_per_90** — Short and medium passes per 90 minutes.  
- **accurate_short_/_medium_passes_%** — Accuracy of short and medium passes.  
- **long_passes_per_90** — Long passes attempted per 90 minutes.  
- **accurate_long_passes_%** — Long pass completion rate.  
- **average_pass_length_m** — Average pass distance in meters.  
- **average_long_pass_length_m** — Average long pass distance.  

## Creative & Progression Passing

- **key_passes_per_90** — Passes leading directly to shots.  
- **shot_assists_per_90** — Assists for shot attempts.  
- **second_assists_per_90** — Passes before the assist.  
- **third_assists_per_90** — Passes before the second assist.  
- **smart_passes_per_90** — Creative passes breaking defensive structure.  
- **accurate_smart_passes_%** — Smart pass success rate.  
- **through_passes_per_90** — Penetrative passes behind defensive line.  
- **accurate_through_passes_%** — Through pass completion rate.  
- **progressive_passes_per_90** — Passes significantly advancing the attack.  
- **accurate_progressive_passes_%** — Progressive pass success rate.  
- **passes_to_final_third_per_90** — Passes into attacking third.  
- **accurate_passes_to_final_third_%** — Accuracy into final third.  
- **passes_to_penalty_area_per_90** — Passes into penalty area.  
- **accurate_passes_to_penalty_area_%** — Accuracy into penalty area.  
- **deep_completions_per_90** — Completed passes near opponent goal.  

## Crossing

- **crosses_per_90** — Cross attempts per 90 minutes.  
- **accurate_crosses_%** — Cross completion rate.  
- **crosses_from_left_flank_per_90** — Crosses from left side.  
- **accurate_crosses_from_left_flank_%** — Accuracy of left crosses.  
- **crosses_from_right_flank_per_90** — Crosses from right side.  
- **accurate_crosses_from_right_flank_%** — Accuracy of right crosses.  
- **crosses_to_goalie_box_per_90** — Crosses delivered into six-yard box.  
- **deep_completed_crosses_per_90** — Completed crosses in deep attacking zones.  

## Receiving

- **received_passes_per_90** — Passes received per 90 minutes.  
- **received_long_passes_per_90** — Long passes received per 90 minutes.  

## Defensive Activity

- **successful_defensive_actions_per_90** — Defensive actions completed successfully.  
- **defensive_duels_per_90** — Defensive duels contested.  
- **defensive_duels_won_%** — Defensive duel success rate.  
- **aerial_duels_per_90** — Aerial challenges contested.  
- **aerial_duels_won_%** — Aerial duel success rate.  
- **sliding_tackles_per_90** — Sliding tackles attempted.  
- **padj_sliding_tackles** — Sliding tackles adjusted for possession context.  
- **interceptions_per_90** — Pass interceptions per 90 minutes.  
- **padj_interceptions** — Interceptions adjusted for possession context.  
- **shots_blocked_per_90** — Opponent shots blocked.  

## Discipline

- **fouls_per_90** — Fouls committed per 90 minutes.  
- **yellow_cards** — Total yellow cards received.  
- **yellow_cards_per_90** — Yellow cards per 90 minutes.  
- **red_cards** — Total red cards received.  
- **red_cards_per_90** — Red cards per 90 minutes.  

## Goalkeeper Metrics

- **conceded_goals** — Goals conceded.  
- **conceded_goals_per_90** — Goals conceded per 90 minutes.  
- **shots_against** — Shots faced.  
- **shots_against_per_90** — Shots faced per 90 minutes.  
- **clean_sheets** — Matches without conceding goals.  
- **save_rate_%** — Percentage of saves made.  
- **xg_against** — Expected goals conceded.  
- **xg_against_per_90** — Expected goals conceded per 90 minutes.  
- **prevented_goals** — Goals prevented versus expected.  
- **prevented_goals_per_90** — Goals prevented per 90 minutes.  
- **back_passes_received_as_gk_per_90** — Back passes received by goalkeeper.  
- **exits_per_90** — Goalkeeper defensive actions outside goal area.  

## Set Pieces

- **free_kicks_per_90** — Free kicks taken per 90 minutes.  
- **direct_free_kicks_per_90** — Direct free kicks attempted.  
- **direct_free_kicks_on_target_%** — Direct free kick accuracy.  
- **corners_per_90** — Corner kicks taken.  
- **penalties_taken** — Total penalties taken.  
- **penalty_conversion_%** — Penalty success rate.  

## League Context

- **league** — Competition identifier.  
- **league_base** — Base dataset league grouping.  
- **league_name** — Competition name.  
- **league_country** — Country of competition.  
- **season** — Season identifier.  