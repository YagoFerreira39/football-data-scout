from html import escape
import re
from textwrap import dedent
from urllib.parse import quote, urlencode

import streamlit as st
import pandas as pd

from src.ratings.rating_profiles import RATING_PROFILE_OPTIONS


class Components:
    PLAYER_LIST_COLUMNS = [
        {
            "key": "player",
            "label": "Player",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "main_position",
            "label": "Position",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "team_within_selected_timeframe",
            "label": "Team",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "birth_country",
            "label": "Nationality",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "league_name",
            "label": "League",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "minutes_played",
            "label": "Minutes Played",
            "width": "0.6fr",
            "align": "center",
        },
    ]
    TEAM_PLAYER_LIST_COLUMNS = [
        {
            "key": "position",
            "label": "Position",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "player",
            "label": "Player",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "age",
            "label": "Age",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "birth_country",
            "label": "Nationality",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "team_within_selected_timeframe",
            "label": "Team",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "on_loan",
            "label": "On Loan",
            "width": "0.6fr",
            "align": "center",
        },
        # {
        #     "key": "season",
        #     "label": "Season",
        #     "width": "0.6fr",
        #     "align": "center",
        # },
        {
            "key": "minutes_played",
            "label": "Minutes",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "matches_played",
            "label": "Matches",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "goals",
            "label": "Goals",
            "width": "0.6fr",
            "align": "center",
        },
        {
            "key": "assists",
            "label": "Assists",
            "width": "0.6fr",
            "align": "center",
        },
    ]
    
    POSITION_FILTER_ORDER = ["GK", "CB", "FB", "DM", "CM", "AM", "WF", "CF"]
    
    @staticmethod
    def render_main_header(filtered_df: pd.DataFrame, country_col: str, league_col: str, team_col: str, player_col: str) -> None:
        """Render the RoleRadar header section with KPI cards."""
        st.markdown(
            """
            <div class="team-header">
                <div class="team-header-title">RoleRadar - Football Data Analysis</div>
                <div class="team-header-meta">
                    <span class="team-header-pill">Explore players by country, league, season and name</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        kpis = [
            ("Countries", filtered_df[country_col].nunique()),
            ("Leagues",   filtered_df[league_col].nunique()),
            ("Teams",     filtered_df[team_col].nunique()),
            ("Players",   filtered_df[player_col].nunique()),
        ]

        for col, (label, value) in zip(st.columns(len(kpis)), kpis):
            with col:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.divider()
    
    @staticmethod
    def render_sidebar_filters(
        df: pd.DataFrame,
        country_col: str,
        league_col: str,
        season_col: str,
        key_prefix: str = "main",
    ) -> tuple[str, str, str, str, str]:
        countries = ["All"] + sorted(
            df[country_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_country = st.sidebar.selectbox(
            "Country",
            countries,
            key=f"{key_prefix}_selected_country",
        ) if key_prefix == "main" else None

        league_df = df.copy()

        if selected_country != "All":
            league_df = league_df[league_df[country_col] == selected_country]

        leagues = ["All"] + sorted(
            league_df[league_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_league = st.sidebar.selectbox(
            "League",
            leagues,
            key=f"{key_prefix}_selected_league",
        ) if key_prefix == "main" else None

        season_df = league_df.copy()

        if selected_league != "All":
            season_df = season_df[season_df[league_col] == selected_league]

        seasons = ["All"] + sorted(
            season_df[season_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist(),
            reverse=True,
        )

        selected_season = st.sidebar.selectbox(
            "Season",
            seasons,
            key=f"{key_prefix}_selected_season",
        ) if key_prefix == "main" else None

        team_search = st.sidebar.text_input(
            "Search team",
            placeholder="Type team name...",
            key=f"{key_prefix}_team_search",
        )

        player_search = st.sidebar.text_input(
            "Search player",
            placeholder="Type player name...",
            key=f"{key_prefix}_player_search",
        )
        
        selected_rating_profile_label = st.sidebar.selectbox(
            "Player Rating Profile",
            options=list(RATING_PROFILE_OPTIONS.keys()),
            index=0,
            key="league_rating_profile",
        )

        minimum_minutes_played = st.sidebar.number_input(
            "Minimum Minutes",
            min_value=0,
            max_value=5000,
            value=1000,
            step=100,
            key="league_rating_min_minutes",
        )

        return (
            selected_country,
            selected_league,
            selected_season,
            team_search,
            player_search,
            selected_rating_profile_label,
            minimum_minutes_played
        )
        
    def render_squad_filters(
        self,
        df: pd.DataFrame,
        position_col: str = "common_position",
        nationality_col: str = "birth_country",
        age_col: str = "age",
        loan_col: str = "on_loan",
        key_prefix: str = "squad",
    ) -> tuple[list[str], str, tuple[int, int], bool]:
        filter_source_df = df.copy()

        filter_source_df[age_col] = pd.to_numeric(
            filter_source_df[age_col],
            errors="coerce",
        )

        available_nationalities = (
            filter_source_df[nationality_col]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
            .tolist()
        )
        
        title_col = st.columns(
            [1.5],
            vertical_alignment="center",
        )[0]
        with title_col:
            if key_prefix == "squad":
                st.markdown("## Squad")
            else:
                st.markdown("## Players")

        positions_col, loan_ui_col, nationality_ui_col, age_ui_col = st.columns(
            [6.5, 1.8, 1.1, 1.8],
            vertical_alignment="center",
        )

        with nationality_ui_col:
            selected_nationality = st.selectbox(
                "Nationality",
                options=["All"] + available_nationalities,
                index=0,
                key=f"{key_prefix}_nationality",
            )

        with loan_ui_col:
            only_on_loan = st.checkbox(
                "Only on loan",
                value=False,
                key=f"{key_prefix}_only_on_loan",
            )

        # Base pool for age slider: nationality + loan filters
        age_range_source_df = filter_source_df.copy()

        if selected_nationality != "All":
            age_range_source_df = age_range_source_df[
                age_range_source_df[nationality_col].eq(selected_nationality)
            ]

        if only_on_loan and loan_col in age_range_source_df.columns:
            age_range_source_df = age_range_source_df[
                age_range_source_df[loan_col].ne("-")
            ]

        valid_ages = age_range_source_df[age_col].dropna()

        if valid_ages.empty:
            min_age = 13
            max_age = 50
        else:
            min_age = int(valid_ages.min())
            max_age = int(valid_ages.max())

        age_range_key = f"{key_prefix}_age_range"
        current_age_range = st.session_state.get(age_range_key)

        if current_age_range:
            current_min_age, current_max_age = current_age_range

            current_min_age = max(current_min_age, min_age)
            current_max_age = min(current_max_age, max_age)
            if current_min_age == current_max_age:
                current_max_age += 1
            
            if current_min_age > current_max_age:
                current_min_age, current_max_age = min_age, max_age

            st.session_state[age_range_key] = (current_min_age, current_max_age)
        else:
            st.session_state[age_range_key] = (min_age, max_age)

        with age_ui_col:
            selected_age_range = st.slider(
                "Age",
                min_value=min_age,
                max_value=max_age,
                value=st.session_state[age_range_key],
                step=1,
                key=age_range_key,
            )

        min_selected_age, max_selected_age = selected_age_range

        # Position counts should reflect nationality + loan + selected age range
        position_count_source_df = age_range_source_df[
            age_range_source_df[age_col].between(
                min_selected_age,
                max_selected_age,
                inclusive="both",
            )
        ]

        position_counts = (
            position_count_source_df[position_col]
            .value_counts()
            .to_dict()
        )

        available_positions = [
            pos for pos in self.POSITION_FILTER_ORDER
            if pos in position_counts
        ]

        selected_positions = []

        with positions_col:
            if available_positions:
                filter_cols = st.columns(len(available_positions))

                for col, position in zip(filter_cols, available_positions):
                    label = f"{position} ({position_counts[position]})"

                    with col:
                        is_selected = st.checkbox(
                            label,
                            value=True,
                            key=f"{key_prefix}_position_{position}",
                        )

                        if is_selected:
                            selected_positions.append(position)

        return selected_positions, selected_nationality, selected_age_range, only_on_loan

    def filter_players(
        self,
        squad_df: pd.DataFrame,
        position_col: str = "common_position",
        nationality_col: str = "birth_country",
        age_col: str = "age",
        loan_col: str = "on_loan",
        key_prefix: str = "players",
    ) -> pd.DataFrame:
        filtered_squad_df = squad_df.copy()

        selected_positions, selected_nationality, selected_age_range, only_on_loan = (
            self.render_squad_filters(
                df=squad_df,
                position_col=position_col,
                nationality_col=nationality_col,
                age_col=age_col,
                loan_col=loan_col,
                key_prefix=key_prefix,
            )
        )

        filtered_squad_df[age_col] = pd.to_numeric(
            filtered_squad_df[age_col],
            errors="coerce",
        )

        if selected_nationality != "All":
            filtered_squad_df = filtered_squad_df[
                filtered_squad_df[nationality_col].eq(selected_nationality)
            ]

        if only_on_loan and loan_col in filtered_squad_df.columns:
            filtered_squad_df = filtered_squad_df[
                filtered_squad_df[loan_col].ne("-")
            ]

        min_selected_age, max_selected_age = selected_age_range

        filtered_squad_df = filtered_squad_df[
            filtered_squad_df[age_col].between(
                min_selected_age,
                max_selected_age,
                inclusive="both",
            )
        ]

        if selected_positions:
            filtered_squad_df = filtered_squad_df[
                filtered_squad_df[position_col].isin(selected_positions)
            ]

        return filtered_squad_df.reset_index(drop=True)
    
    def render_league_grid(
        self,
        leagues_df: pd.DataFrame,
        league_col: str,
        country_col: str,
    ) -> None:
        cards_html = ""

        for _, row in leagues_df.iterrows():
            league_name = row[league_col]
            league_country = row[country_col]
            league_seasons = row["seasons_display"]
            league_initials = self.__get_initials(league_name)

            league_url = self.__build_league_url(
                country=league_country,
                league=league_name,
            )
            
            cards_html += f"""
            <a class="entity-card" href="{league_url}" target="_self">
                <div class="entity-card-top">
                    <div class="entity-card-badge">{escape(league_initials)}</div>
                    <div class="entity-card-title">{escape(str(league_name))}</div>
                </div>
                <div class="entity-card-meta">
                    <span class="entity-card-country">{escape(str(league_country))}</span>
                    <span class="entity-card-seasons">{escape(str(league_seasons))}</span>
                </div>
            </a>
            """

        st.markdown(
            f"""
            <div class="entity-grid">
                {cards_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    def render_teams_grid(
        self,
        teams_df: pd.DataFrame,
        team_col: str,
        league_col: str,
        country_col: str,
        season_col: str,
    ) -> None:
        cards_html = ""

        for _, row in teams_df.iterrows():
            team_name = row[team_col]
            team_league = row[league_col]
            team_country = row[country_col]
            team_season = row[season_col]

            team_url = self.__build_team_url(
                country=team_country,
                league=team_league,
                season=team_season,  
                team=team_name,
            )

            team_initials = self.__get_initials(team_name)

            cards_html += f"""
            <a class="entity-card" href="{team_url}" target="_self">
                <div class="entity-card-top">
                    <div class="entity-card-badge">{escape(team_initials)}</div>
                    <div class="entity-card-title">{escape(str(team_name))}</div>
                </div>
                <div class="entity-card-subtitle">{escape(str(team_country))} - {escape(str(team_season))}</div>
            </a>
            """

        st.markdown(
            f"""
            <div class="entity-grid">
                {cards_html}
            </div>
            """,
            unsafe_allow_html=True,
        ) 
        
    def render_players_list(
        self,
        players_df: pd.DataFrame,
        default_sort_col: str,
        show_minutes_played: bool = True,
    ) -> None:
        columns_config = self.PLAYER_LIST_COLUMNS
        if not show_minutes_played:
            columns_config = [col for col in columns_config if col["key"] != "minutes_played"]
        
        self._render_players_table(
            players_df=players_df,
            columns_config=columns_config,
            default_sort_col=default_sort_col,
            sort_state_prefix="main_players",
        )
        
    def render_team_players_list(
        self,
        players_df: pd.DataFrame,
        default_sort_col: str = "minutes_played",
        show_current_team: bool = True,
    ) -> None:
        columns_config = self.TEAM_PLAYER_LIST_COLUMNS
        if not show_current_team:
            columns_config = [col for col in columns_config if col["key"] != "team_within_selected_timeframe"]
            
        self._render_players_table(
            players_df=players_df,
            columns_config=columns_config,
            default_sort_col=default_sort_col,
            sort_state_prefix="team_players",
        )
    
    @staticmethod
    def __slugify(value: str) -> str:
        value = str(value).lower().strip()
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-")

    def __build_league_url(
        self,
        country: str,
        league: str,
    ) -> str:
        query_params = urlencode(
            {
                "country": self.__slugify(country),
                "league": self.__slugify(league),
            }
        )

        return f"/leagues?{query_params}"
    
    def __build_team_url(
        self,
        country: str,
        league: str,
        season: str,
        team: str,
    ) -> str:
        query_params = urlencode(
            {
                "country": self.__slugify(country),
                "league": self.__slugify(league),
                "season": self.__slugify(season),
                "team": self.__slugify(team),
            }
        )

        return f"/teams?{query_params}"
    
    def __build_player_url(self, player: str, team: str, season: str) -> str:
        query_params = urlencode(
            {
                "player": self.__slugify(player),
                "team": self.__slugify(team),
                "season": self.__slugify(season),
            }
        )

        return f"/players?{query_params}"

    @staticmethod
    def __get_initials(value: str, max_letters: int = 2) -> str:
        words = str(value).replace("-", " ").split()

        if not words:
            return "?"

        return "".join(word[0] for word in words[:max_letters]).upper()

    @staticmethod
    def get_current_sort_state(
        default_sort_col: str,
        sort_state_prefix: str = "players",
        default_ascending: bool = True,
    ) -> tuple[str, bool]:
        sort_col_key = f"{sort_state_prefix}_sort_col"
        sort_ascending_key = f"{sort_state_prefix}_sort_ascending"

        if sort_col_key not in st.session_state:
            st.session_state[sort_col_key] = default_sort_col

        if sort_ascending_key not in st.session_state:
            st.session_state[sort_ascending_key] = default_ascending

        return (
            st.session_state[sort_col_key],
            st.session_state[sort_ascending_key],
        )


    @staticmethod
    def update_sort_state(
        column: str,
        sort_state_prefix: str = "players",
    ) -> None:
        sort_col_key = f"{sort_state_prefix}_sort_col"
        sort_ascending_key = f"{sort_state_prefix}_sort_ascending"

        current_col = st.session_state.get(sort_col_key)
        current_ascending = st.session_state.get(sort_ascending_key, True)

        if current_col == column:
            st.session_state[sort_ascending_key] = not current_ascending
        else:
            st.session_state[sort_col_key] = column
            st.session_state[sort_ascending_key] = True


    def sort_players_df(
        self,
        players_df: pd.DataFrame,
        sort_col: str,
        ascending: bool,
    ) -> pd.DataFrame:
        if sort_col not in players_df.columns:
            return players_df

        return (
            players_df
            .sort_values(sort_col, ascending=ascending, na_position="last")
            .reset_index(drop=True)
        )
    
    def render_players_header(
        self,
        columns_config: list[dict],
        default_sort_col: str,
        sort_state_prefix: str = "players",
        default_ascending: bool = True,
    ) -> None:
        sort_col, ascending = self.get_current_sort_state(
            default_sort_col=default_sort_col,
            sort_state_prefix=sort_state_prefix,
            default_ascending=default_ascending
        )

        column_widths = [
            col_config.get("streamlit_width", 1)
            for col_config in columns_config
        ]

        header_cols = st.columns(column_widths)

        for header_col, col_config in zip(header_cols, columns_config):
            col_key = col_config["key"]
            label = col_config["label"]

            sort_icon = ""
            if col_key == sort_col:
                sort_icon = " ↑" if ascending else " ↓"

            with header_col:
                if st.button(
                    f"{label}{sort_icon}",
                    key=f"{sort_state_prefix}_sort_{col_key}",
                    use_container_width=True,
                ):
                    self.update_sort_state(
                        column=col_key,
                        sort_state_prefix=sort_state_prefix,
                    )
                    st.rerun()
                    
    def render_players_rows(
        self,
        players_df: pd.DataFrame,
        columns_config: list[dict],
    ) -> None:
        grid_template = " ".join(
            col_config.get("width", "1fr")
            for col_config in columns_config
        )

        rows = []

        for _, row in players_df.iterrows():
            row_cells = []
            player_name = row.get("player", "")
            season = row.get("season", "")
            team = row.get("team_within_selected_timeframe", "")
            player_url = self.__build_player_url(
                player=str(player_name),
                season=str(season),
                team=str(team),
            )

            for col_config in columns_config:
                col = col_config["key"]
                align = col_config.get("align", "center")
                value = row.get(col, "-")
                if col == "age":
                    value = int(value) if pd.notna(value) else "-"

                if pd.isna(value):
                    value = "-"

                row_cells.append(
                    f'<div class="player-list-cell align-{align}">'
                    f'{escape(str(value))}'
                    f'</div>'
                )

            rows.append(
                f'<a class="player-list-row player-list-row-link" '
                f'href="{player_url}" target="_self" '
                f'style="grid-template-columns: {grid_template};">'
                f'{"".join(row_cells)}'
                f'</a>'
            )

        html = (
            '<div class="player-list-wrapper">'
            '<div class="player-list-body">'
            f'{"".join(rows)}'
            '</div>'
            '</div>'
        )

        st.markdown(html, unsafe_allow_html=True)
        
    def _render_players_table(
        self,
        players_df: pd.DataFrame,
        columns_config: list[dict],
        default_sort_col: str,
        sort_state_prefix: str = "players",
    ) -> None:
        self.render_players_header(
            columns_config=columns_config,
            default_sort_col=default_sort_col,
            sort_state_prefix=sort_state_prefix,
        )

        sort_col, ascending = self.get_current_sort_state(
            default_sort_col=default_sort_col,
            sort_state_prefix=sort_state_prefix,
        )

        sorted_df = self.sort_players_df(
            players_df=players_df,
            sort_col=sort_col,
            ascending=ascending,
        )

        self.render_players_rows(
            players_df=sorted_df,
            columns_config=columns_config,
        )
        
    from html import escape

    def __format_rating_column_label(self, column: str) -> str:
        label = str(column)

        if label.lower().endswith("_att"):
            label = label[:-4]

        label = label.replace("_", " ")

        return label.title()
    
    # RENDER PLAYER RATINGS TABLE
    def __format_rating_column_label(self, column: str) -> str:
        label = str(column)

        if label.lower().endswith("_att"):
            label = label[:-4]

        label = label.replace("_", " ")

        return label.title()


    def __format_rating_value(self, value) -> str:
        if pd.isna(value):
            return "-"

        try:
            return f"{float(value):.2f}"
        except (TypeError, ValueError):
            return str(value)
        
    def __format_rating_column_label(self, column: str) -> str:
        label = str(column)

        if label.lower().endswith("_att"):
            label = label[:-4]

        label = label.replace("_", " ")

        return label.title()


    def __format_rating_value(self, value) -> str:
        if pd.isna(value):
            return "-"

        try:
            return f"{float(value):.2f}"
        except (TypeError, ValueError):
            return str(value)


    def __get_rating_sort_indicator(
        self,
        column: str,
        current_sort_col: str | None,
        current_sort_direction: str,
    ) -> str:
        if column != current_sort_col:
            return ""

        return " ↑" if current_sort_direction == "asc" else " ↓"


    def __sort_ratings_df(
        self,
        ratings_df: pd.DataFrame,
        sort_col: str,
        sort_direction: str,
    ) -> pd.DataFrame:
        if ratings_df.empty or sort_col not in ratings_df.columns:
            return ratings_df

        ascending = sort_direction == "asc"

        return (
            ratings_df
            .sort_values(
                by=sort_col,
                ascending=ascending,
                na_position="last",
                kind="mergesort",
            )
            .reset_index(drop=True)
        )
        
    def __get_rating_column_config(self, ratings_df: pd.DataFrame) -> list[dict]:
        column_aliases = {
            "rank": "Rank",
            "player": "Player",
            "team_within_selected_timeframe": "Team",
            "team": "Team",
            "main_position": "Position",
            "position": "Position",
            "age": "Age",
            "minutes_played": "Minutes",
            "overall_rating": "Overall",
        }

        preferred_order = [
            "rank",
            "player",
            "team_within_selected_timeframe",
            "team",
            "main_position",
            "position",
            "age",
            "minutes_played",
        ]

        width_by_column = {
            "rank": "0.55fr",
            "player": "1.35fr",
            "team_within_selected_timeframe": "1.65fr",
            "team": "1.65fr",
            "main_position": "0.75fr",
            "position": "0.75fr",
            "age": "0.55fr",
            "minutes_played": "0.85fr",
            "overall_rating": "0.85fr",
        }

        columns_config = []

        for column in preferred_order:
            if column not in ratings_df.columns:
                continue

            columns_config.append(
                {
                    "key": column,
                    "label": column_aliases.get(
                        column,
                        self.__format_rating_column_label(column),
                    ),
                    "width": width_by_column.get(column, "1fr"),
                    "align": (
                        "left"
                        if column in {"player", "team", "team_within_selected_timeframe"}
                        else "center"
                    ),
                    "is_rating": False,
                }
            )

        rating_columns = [
            column
            for column in ratings_df.columns
            if column.lower().endswith("_att")
        ]

        for column in rating_columns:
            columns_config.append(
                {
                    "key": column,
                    "label": self.__format_rating_column_label(column),
                    "width": "1.15fr",
                    "align": "center",
                    "is_rating": True,
                }
            )

        if "overall_rating" in ratings_df.columns:
            columns_config.append(
                {
                    "key": "overall_rating",
                    "label": "Overall",
                    "width": width_by_column["overall_rating"],
                    "align": "center",
                    "is_rating": True,
                    "is_overall": True,
                }
            )

        return columns_config
    
    def render_player_ratings_list(
        self,
        ratings_df: pd.DataFrame,
        title: str = "Player Ratings",
        default_sort_col: str = "overall_rating",
        default_sort_direction: str = "desc",
        key_prefix: str = "ratings",
    ) -> None:
        if ratings_df.empty:
            st.info("No players found for the selected rating profile and minimum minutes.")
            return

        columns_config = self.__get_rating_column_config(ratings_df)

        available_sort_columns = [
            col_config["key"]
            for col_config in columns_config
            if col_config["key"] not in ["player", "rank", "team_within_selected_timeframe", "main_position"]
        ]

        if default_sort_col not in available_sort_columns:
            default_sort_col = available_sort_columns[0]

        sort_col_key = f"{key_prefix}_sort_col"
        sort_direction_key = f"{key_prefix}_sort_direction"

        if sort_col_key not in st.session_state:
            st.session_state[sort_col_key] = default_sort_col

        if sort_direction_key not in st.session_state:
            st.session_state[sort_direction_key] = default_sort_direction

        current_sort_col = st.session_state[sort_col_key]
        current_sort_direction = st.session_state[sort_direction_key]

        if current_sort_col not in available_sort_columns:
            current_sort_col = default_sort_col
            st.session_state[sort_col_key] = default_sort_col

        ratings_df = self.__sort_ratings_df(
            ratings_df=ratings_df,
            sort_col=current_sort_col,
            sort_direction=current_sort_direction,
        )

        grid_template = " ".join(
            col_config.get("width", "1fr")
            for col_config in columns_config
        )

        # =========================
        # Title
        # =========================

        st.markdown(
            f"""
            <div class="rating-list-title">{escape(title)}</div>
            """,
            unsafe_allow_html=True,
        )

        # =========================
        # Sort controls, compact
        # =========================

        sort_col_1, sort_col_2, _ = st.columns(
            [1.6, 1.6, 6.8],
            vertical_alignment="center",
        )

        with sort_col_1:
            selected_sort_col = st.selectbox(
                "Sort by",
                options=available_sort_columns,
                format_func=lambda col: next(
                    config["label"]
                    for config in columns_config
                    if config["key"] == col
                ),
                index=available_sort_columns.index(current_sort_col),
                key=f"{key_prefix}_sort_select",
            )

        with sort_col_2:
            selected_sort_direction = st.segmented_control(
                "Direction",
                options=["desc", "asc"],
                default=current_sort_direction,
                format_func=lambda value: "Desc" if value == "desc" else "Asc",
                key=f"{key_prefix}_sort_direction_select",
            )

        st.session_state[sort_col_key] = selected_sort_col
        st.session_state[sort_direction_key] = selected_sort_direction

        ratings_df = self.__sort_ratings_df(
            ratings_df=ratings_df,
            sort_col=selected_sort_col,
            sort_direction=selected_sort_direction,
        )

        # =========================
        # Header
        # =========================

        header_cells = ""

        for col_config in columns_config:
            column = col_config["key"]
            align = col_config.get("align", "center")

            extra_classes = []

            if column == "overall_rating":
                extra_classes.append("is-overall")

            extra_class = f" {' '.join(extra_classes)}" if extra_classes else ""

            sort_indicator = self.__get_rating_sort_indicator(
                column=column,
                current_sort_col=selected_sort_col,
                current_sort_direction=selected_sort_direction,
            )

            header_cells += (
                f'<div class="rating-list-header-cell align-{align}{extra_class}">'
                f'{escape(col_config["label"] + sort_indicator)}'
                f'</div>'
            )

        # =========================
        # Rows
        # =========================

        rows_html = ""

        for _, row in ratings_df.iterrows():
            row_cells = ""

            for col_config in columns_config:
                column = col_config["key"]
                align = col_config.get("align", "center")
                value = row.get(column, "-")

                extra_classes = []

                if column == "overall_rating":
                    extra_classes.append("is-overall")

                if column == "rank":
                    extra_classes.append("is-rank")

                if column == "player":
                    extra_classes.append("is-player")

                if col_config.get("is_rating"):
                    extra_classes.append("is-rating")

                extra_class = f" {' '.join(extra_classes)}" if extra_classes else ""

                if column in {"rank", "age", "minutes_played"} and pd.notna(value):
                    value = int(value)

                elif col_config.get("is_rating"):
                    value = self.__format_rating_value(value)

                elif pd.isna(value):
                    value = "-"

                row_cells += (
                    f'<div class="rating-list-cell align-{align}{extra_class}">'
                    f'{escape(str(value))}'
                    f'</div>'
                )

            rows_html += f"""
            <div class="rating-list-row" style="grid-template-columns: {grid_template};">
                {row_cells}
            </div>
            """

        st.markdown(
            f"""
            <div class="rating-list-container">
                <div class="rating-list-header" style="grid-template-columns: {grid_template};">
                    {header_cells}
                </div>

                {rows_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


    # def __get_rating_column_config(self, ratings_df: pd.DataFrame) -> list[dict]:
    #     column_aliases = {
    #         "rank": "Rank",
    #         "player": "Player",
    #         "team_within_selected_timeframe": "Team",
    #         "team": "Team",
    #         "main_position": "Position",
    #         "position": "Position",
    #         "age": "Age",
    #         "minutes_played": "Minutes",
    #         "overall_rating": "Overall",
    #     }

    #     preferred_order = [
    #         "rank",
    #         "player",
    #         "team_within_selected_timeframe",
    #         "team",
    #         "main_position",
    #         "position",
    #         "age",
    #         "minutes_played",
    #     ]

    #     width_by_column = {
    #         "rank": "0.75fr",
    #         "player": "1.35fr",
    #         "team_within_selected_timeframe": "1.60fr",
    #         "team": "1.60fr",
    #         "main_position": "0.95fr",
    #         "position": "0.95fr",
    #         "age": "0.75fr",
    #         "minutes_played": "1.00fr",
    #         "overall_rating": "1.00fr",
    #     }

    #     streamlit_width_by_column = {
    #         "rank": 0.75,
    #         "player": 1.35,
    #         "team_within_selected_timeframe": 1.60,
    #         "team": 1.60,
    #         "main_position": 0.95,
    #         "position": 0.95,
    #         "age": 0.75,
    #         "minutes_played": 1.00,
    #         "overall_rating": 1.00,
    #     }

    #     columns_config = []

    #     for column in preferred_order:
    #         if column not in ratings_df.columns:
    #             continue

    #         columns_config.append(
    #             {
    #                 "key": column,
    #                 "label": column_aliases.get(
    #                     column,
    #                     self.__format_rating_column_label(column),
    #                 ),
    #                 "width": width_by_column.get(column, "1fr"),
    #                 "streamlit_width": streamlit_width_by_column.get(column, 1.0),
    #                 "align": (
    #                     "left"
    #                     if column in {"player", "team", "team_within_selected_timeframe"}
    #                     else "center"
    #                 ),
    #                 "is_rating": False,
    #             }
    #         )

    #     rating_columns = [
    #         column
    #         for column in ratings_df.columns
    #         if column.lower().endswith("_att")
    #     ]

    #     for column in rating_columns:
    #         columns_config.append(
    #             {
    #                 "key": column,
    #                 "label": self.__format_rating_column_label(column),
    #                 "width": "1.20fr",
    #                 "streamlit_width": 1.20,
    #                 "align": "center",
    #                 "is_rating": True,
    #             }
    #         )

    #     if "overall_rating" in ratings_df.columns:
    #         columns_config.append(
    #             {
    #                 "key": "overall_rating",
    #                 "label": "Overall",
    #                 "width": width_by_column["overall_rating"],
    #                 "streamlit_width": streamlit_width_by_column["overall_rating"],
    #                 "align": "center",
    #                 "is_rating": True,
    #                 "is_overall": True,
    #             }
    #         )

    #     return columns_config


    # def sort_ratings_df(
    #     self,
    #     ratings_df: pd.DataFrame,
    #     sort_col: str,
    #     ascending: bool,
    # ) -> pd.DataFrame:
    #     if sort_col not in ratings_df.columns:
    #         return ratings_df

    #     return (
    #         ratings_df
    #         .sort_values(
    #             by=sort_col,
    #             ascending=ascending,
    #             na_position="last",
    #             kind="mergesort",
    #         )
    #         .reset_index(drop=True)
    #     )


    # def render_ratings_header(
    #     self,
    #     columns_config: list[dict],
    #     default_sort_col: str,
    #     sort_state_prefix: str = "ratings",
    #     default_ascending: bool = False,
    # ) -> None:
    #     sort_col, ascending = self.get_current_sort_state(
    #         default_sort_col=default_sort_col,
    #         sort_state_prefix=sort_state_prefix,
    #         default_ascending=False,
    #     )

    #     column_widths = [
    #         col_config.get("streamlit_width", 1)
    #         for col_config in columns_config
    #     ]

    #     header_cols = st.columns(column_widths)

    #     for header_col, col_config in zip(header_cols, columns_config):
    #         col_key = col_config["key"]
    #         label = col_config["label"]

    #         sort_icon = ""
    #         if col_key == sort_col:
    #             sort_icon = " ↑" if ascending else " ↓"

    #         with header_col:
    #             if st.button(
    #                 f"{label}{sort_icon}",
    #                 key=f"{sort_state_prefix}_sort_{col_key}",
    #                 use_container_width=True,
    #             ):
    #                 self.update_sort_state(
    #                     column=col_key,
    #                     sort_state_prefix=sort_state_prefix,
    #                 )
    #                 st.rerun()


    # def render_ratings_rows(
    #     self,
    #     ratings_df: pd.DataFrame,
    #     columns_config: list[dict],
    # ) -> None:
    #     grid_template = " ".join(
    #         col_config.get("width", "1fr")
    #         for col_config in columns_config
    #     )

    #     rows = []

    #     for _, row in ratings_df.iterrows():
    #         row_cells = []

    #         for col_config in columns_config:
    #             column = col_config["key"]
    #             align = col_config.get("align", "center")
    #             value = row.get(column, "-")

    #             extra_classes = []

    #             if column == "rank":
    #                 extra_classes.append("is-rank")

    #             if column == "player":
    #                 extra_classes.append("is-player")

    #             if col_config.get("is_rating"):
    #                 extra_classes.append("is-rating")

    #             if column == "overall_rating":
    #                 extra_classes.append("is-overall")

    #             extra_class = f" {' '.join(extra_classes)}" if extra_classes else ""

    #             if column in {"rank", "age", "minutes_played"} and pd.notna(value):
    #                 value = int(value)

    #             elif col_config.get("is_rating"):
    #                 value = self.__format_rating_value(value)

    #             elif pd.isna(value):
    #                 value = "-"

    #             row_cells.append(
    #                 f'<div class="rating-list-cell align-{align}{extra_class}">'
    #                 f'{escape(str(value))}'
    #                 f'</div>'
    #             )

    #         rows.append(
    #             f'<div class="rating-list-row" '
    #             f'style="grid-template-columns: {grid_template};">'
    #             f'{"".join(row_cells)}'
    #             f'</div>'
    #         )

    #     html = (
    #         '<div class="rating-list-wrapper">'
    #         '<div class="rating-list-body">'
    #         f'{"".join(rows)}'
    #         '</div>'
    #         '</div>'
    #     )

    #     st.markdown(html, unsafe_allow_html=True)


    # def render_player_ratings_list(
    #     self,
    #     ratings_df: pd.DataFrame,
    #     title: str = "Player Ratings",
    #     default_sort_col: str = "overall_rating",
    #     sort_state_prefix: str = "ratings",
    # ) -> None:
    #     if ratings_df.empty:
    #         st.info("No players found for the selected rating profile and minimum minutes.")
    #         return

    #     columns_config = self.__get_rating_column_config(ratings_df)

    #     available_columns = [
    #         col_config["key"]
    #         for col_config in columns_config
    #     ]

    #     if default_sort_col not in available_columns:
    #         default_sort_col = available_columns[0]

    #     st.markdown(
    #         f"""
    #         <div class="rating-list-title">{escape(title)}</div>
    #         """,
    #         unsafe_allow_html=True,
    #     )

    #     self.render_ratings_header(
    #         columns_config=columns_config,
    #         default_sort_col=default_sort_col,
    #         sort_state_prefix=sort_state_prefix,
    #         default_ascending=False
    #     )

    #     sort_col, ascending = self.get_current_sort_state(
    #         default_sort_col=default_sort_col,
    #         sort_state_prefix=sort_state_prefix,
    #     )

    #     sorted_df = self.sort_ratings_df(
    #         ratings_df=ratings_df,
    #         sort_col=sort_col,
    #         ascending=ascending,
    #     )

    #     self.render_ratings_rows(
    #         ratings_df=sorted_df,
    #         columns_config=columns_config,
    #     )
        