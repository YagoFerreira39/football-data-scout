# =========================
# TEAM HEADER UI
# =========================

import pandas as pd
import streamlit as st


def _get_badge_url(row: pd.Series) -> str | None:
    """
    Gets the best available badge URL from a team row.
    """

    for col in ["badge_lg", "badge_sm"]:
        if col in row.index and pd.notna(row[col]) and row[col]:
            return row[col]

    return None


def render_team_header_from_row(
    row: pd.Series,
    *,
    title_col: str = "contestant_name",
) -> None:
    """
    Renders a reusable team header with badge, team name and context.
    """

    badge_url = _get_badge_url(row)

    team_name = row.get(title_col, "Team")
    league_name = row.get("source_league_name", "")
    country_name = row.get("source_country_name", "")
    season = row.get("source_season", "")

    badge_col, text_col = st.columns([1, 7])

    with badge_col:
        if badge_url:
            st.image(badge_url, width=78)

    with text_col:
        st.markdown(f"## {team_name}")
        st.caption(
            " | ".join(
                value for value in [country_name, league_name, season]
                if value
            )
        )