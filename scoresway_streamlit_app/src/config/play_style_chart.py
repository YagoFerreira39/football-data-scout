# =========================
# PLAY STYLE CHART CONFIG
# =========================

from src.config.team_style import (
    TEAM_STYLE_SCORE_COLUMNS,
    TEAM_STYLE_SCORE_LABELS,
)


PLAY_STYLE_CHART_SCORE_COLUMNS = [
    col for col in TEAM_STYLE_SCORE_COLUMNS
    if col != "overall_style_intensity_score"
]


PLAY_STYLE_CHART_LABELS = {
    col: TEAM_STYLE_SCORE_LABELS[col]
    for col in PLAY_STYLE_CHART_SCORE_COLUMNS
    if col in TEAM_STYLE_SCORE_LABELS
}


PLAY_STYLE_COMPARISON_OPTIONS = {
    "League average": "league_average",
    "Selected team": "selected_team",
}