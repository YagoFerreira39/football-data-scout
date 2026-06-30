# =========================
# TEAM METRICS
# =========================

import pandas as pd


def safe_divide(
    numerator: pd.Series,
    denominator: pd.Series,
) -> pd.Series:
    """
    Divide safely by replacing zero denominators with NA.
    """

    return numerator / denominator.replace(0, pd.NA)


def add_team_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add basic derived metrics for Scoresway team stats.

    These are row-level calculations, so they are safe to apply
    to all leagues together.
    """

    df = df.copy()

    if "Games Played" not in df.columns:
        return df

    games = df["Games Played"].replace(0, pd.NA)

    per_game_columns = {
        "Goals": "goals_per_game",
        "Goals Conceded": "goals_conceded_per_game",
        "Total Shots": "shots_per_game",
        "Total Shots Conceded": "shots_conceded_per_game",
        "Shots On Target ( inc goals )": "shots_on_target_per_game",
        "Key Passes (Attempt Assists)": "key_passes_per_game",
        "Shots Created": "shots_created_per_game",
        "Total Passes": "passes_per_game",
        "Open Play Passes": "open_play_passes_per_game",
        "Final Third Touches": "final_third_touches_per_game",
        "Duels": "duels_per_game",
        "Aerial Duels": "aerial_duels_per_game",
        "Ground Duels": "ground_duels_per_game",
        "Recoveries": "recoveries_per_game",
        "Interceptions": "interceptions_per_game",
        "Total Clearances": "clearances_per_game",
        "Blocks": "blocks_per_game",
        "Corners Taken (incl short corners)": "corners_taken_per_game",
        "Set Pieces Goals": "set_piece_goals_per_game",
    }

    for raw_col, new_col in per_game_columns.items():
        if raw_col in df.columns:
            df[new_col] = df[raw_col] / games

    if {"Goals", "Goals Conceded"}.issubset(df.columns):
        df["goal_difference_per_game"] = (
            df["Goals"] - df["Goals Conceded"]
        ) / games

    if {"Total Shots", "Total Shots Conceded"}.issubset(df.columns):
        df["shot_difference_per_game"] = (
            df["Total Shots"] - df["Total Shots Conceded"]
        ) / games

    if {"Goals", "Total Shots"}.issubset(df.columns):
        df["goal_conversion_pct"] = (
            safe_divide(df["Goals"], df["Total Shots"]) * 100
        )

    if {"Shots On Target ( inc goals )", "Total Shots"}.issubset(df.columns):
        df["shots_on_target_pct"] = (
            safe_divide(df["Shots On Target ( inc goals )"], df["Total Shots"]) * 100
        )

    if {"Duels won", "Duels"}.issubset(df.columns):
        df["duels_won_pct"] = (
            safe_divide(df["Duels won"], df["Duels"]) * 100
        )

    if {"Aerial Duels won", "Aerial Duels"}.issubset(df.columns):
        df["aerial_duels_won_pct"] = (
            safe_divide(df["Aerial Duels won"], df["Aerial Duels"]) * 100
        )

    if {"Ground Duels won", "Ground Duels"}.issubset(df.columns):
        df["ground_duels_won_pct"] = (
            safe_divide(df["Ground Duels won"], df["Ground Duels"]) * 100
        )

    if {
        "Total Successful Passes ( Excl Crosses & Corners )",
        "Total Passes",
    }.issubset(df.columns):
        df["pass_accuracy_pct"] = (
            safe_divide(
                df["Total Successful Passes ( Excl Crosses & Corners )"],
                df["Total Passes"],
            )
            * 100
        )

    if {"Clean Sheets", "Games Played"}.issubset(df.columns):
        df["clean_sheet_rate_pct"] = (
            safe_divide(df["Clean Sheets"], df["Games Played"]) * 100
        )

    return df