# =========================
# SIMILAR TEAMS CONFIG
# =========================

from src.config.team_style import TEAM_STYLE_SCORE_COLUMNS


SIMILAR_TEAM_SCORE_COLUMNS = [
    col for col in TEAM_STYLE_SCORE_COLUMNS
    if col != "overall_style_intensity_score"
]


SIMILAR_TEAM_SCOPE_OPTIONS = {
    "Same league-season": "same_league_season",
    "Same country-season": "same_country_season",
    "Same season": "same_season",
    "All available teams": "all",
}


SIMILAR_TEAMS_OUTPUT_COLUMNS = [
    "contestant_name",
    "source_country_name",
    "source_league_name",
    "source_season",
    "similarity_score",
    "style_distance",
]