from pathlib import Path
import re

import numpy as np
import pandas as pd

from src import league_map

class WyscoutDataLoader:    
    __data_path = Path(
        "/home/yagoferr/code/personal/football-analysis-scout/football-data-scout/external_data/Wyscout_League_Export.csv"
    )
    __raw_df = pd.read_csv(__data_path)
    
    # POSITION_TO_ROLE = {
    #     "GK": "GK",

    #     "CB": "CB",
    #     "LCB": "CB",
    #     "RCB": "CB",

    #     "LB": "FB",
    #     "RB": "FB",
    #     "LWB": "FB",
    #     "RWB": "FB",

    #     "DMF": "DM",
    #     "LDMF": "DM",
    #     "RDMF": "DM",

    #     "CMF": "CM",
    #     "LCMF": "CM",
    #     "RCMF": "CM",

    #     "AMF": "AM",

    #     "LAMF": "WF",
    #     "RAMF": "WF",
    #     "LW": "WF",
    #     "RW": "WF",
    #     "LWF": "WF",
    #     "RWF": "WF",

    #     "CF": "CF",
    # }
    
    def __safe_divide(self, numerator: pd.Series, denominator: pd.Series) -> pd.Series:
        denominator = denominator.replace(0, np.nan)
        return numerator / denominator


    def prepare_wyscout_data(self) -> pd.DataFrame:
        df = self.__raw_df.copy()

        df.columns = (
            df.columns
            .str.lower()
            .str.replace(",", "", regex=False)
            .str.replace(" ", "_", regex=False)
        )
        
        df["common_position"] = (
            df["position"]
            .map(self.POSITION_TO_ROLE)
            .fillna(df["position"])
        )

        df["league_base"] = df["league"].str.replace(
            r"\s\d{4}(-\d{2})?$",
            "",
            regex=True,
        )

        df["league_name"] = df["league_base"].map(
            lambda x: league_map.league_map.get(x, (None, None))[0]
        )

        df["league_country"] = df["league_base"].map(
            lambda x: league_map.league_map.get(x, (None, None))[1]
        )

        df["league_country"] = df["league_country"].fillna("Unknown")

        df["season"] = df["league"].str.extract(r"(\d{4}(?:-\d{2})?)$")

        df["positions"] = df["position"]
        df["position"] = df["position"].str.split(",").str[0].str.strip()

        df["xa_per_100_passes"] = (
            self.__safe_divide(df["xa_per_90"], df["passes_per_90"]) * 100
        )

        df["xa_per_cross"] = self.__safe_divide(
            df["xa_per_90"],
            df["crosses_per_90"],
        )

        df["crosses_share_of_passes_%"] = (
            self.__safe_divide(df["crosses_per_90"], df["passes_per_90"]) * 100
        )

        df["key_passes_per_100_passes"] = (
            self.__safe_divide(df["key_passes_per_90"], df["passes_per_90"]) * 100
        )

        df["non_penalty_xg"] = df["xg"] - (df["penalties_taken"] * 0.76)
        df["non_penalty_xg"] = df["non_penalty_xg"].clip(lower=0)

        df["non_penalty_xg_per_90"] = (
            self.__safe_divide(df["non_penalty_xg"], df["minutes_played"]) * 90
        )

        df["player_slug"] = df["player"].apply(self.slugify)
        df["league_slug"] = df["league_name"].apply(self.slugify)
        df["team_slug"] = df["team_within_selected_timeframe"].apply(self.slugify)
        df["season_slug"] = df["season"].apply(self.slugify)
        
        # df["common_position"] = (
        #     df["position"]
        #     .map(self.POSITION_TO_ROLE)
        #     .fillna(df["position"])
        # )

        return df
    
    @staticmethod
    def filter_and_sort_leagues_df(
        filtered_df: pd.DataFrame,
        league_col: str,
        country_col: str,
        season_col: str,
        priority_league_order: dict[str, int],
    ) -> pd.DataFrame:
        leagues_df = (
            filtered_df[[league_col, country_col, season_col]]
            .drop_duplicates()
            .groupby([league_col, country_col], as_index=False)
            .agg(
                seasons=(season_col, lambda values: sorted(values.dropna().unique(), reverse=True)),
            )
        )

        leagues_df["seasons_count"] = leagues_df["seasons"].apply(len)
        leagues_df["seasons_display"] = leagues_df["seasons"].apply(
            lambda seasons: " | ".join(map(str, seasons))
        )

        leagues_df["_priority_order"] = leagues_df[league_col].map(priority_league_order)
        leagues_df["_is_priority"] = leagues_df["_priority_order"].notna()

        leagues_df = (
            leagues_df
            .sort_values(
                by=["_is_priority", "_priority_order", league_col, country_col],
                ascending=[False, True, True, True],
            )
            .drop(columns=["_priority_order", "_is_priority"])
            .reset_index(drop=True)
        )

        return leagues_df
    
    POSITION_TO_ROLE = {
        "GK": "GK",

        "CB": "CB",
        "LCB": "CB",
        "RCB": "CB",

        "LB": "FB",
        "RB": "FB",
        "LWB": "FB",
        "RWB": "FB",

        "DMF": "DM",
        "LDMF": "DM",
        "RDMF": "DM",

        "CMF": "CM",
        "LCMF": "CM",
        "RCMF": "CM",

        "AMF": "AM",

        "LAMF": "WF",
        "RAMF": "WF",
        "LW": "WF",
        "RW": "WF",
        "LWF": "WF",
        "RWF": "WF",

        "CF": "CF",
    }


    def build_squad_df(
        self,
        team_df: pd.DataFrame,
        squad_columns: list[str],
        player_col: str = "player",
        minutes_col: str = "minutes_played",
        position_col: str = "position",
        current_team_col: str = "team_within_selected_timeframe",
        original_team_col: str = "team",
    ) -> pd.DataFrame:
        available_columns = [
            col for col in squad_columns
            if col in team_df.columns
        ]

        squad_df = (
            team_df[available_columns]
            .drop_duplicates()
            .sort_values([minutes_col, player_col], ascending=[False, True])
            .reset_index(drop=True)
        )

        if position_col in squad_df.columns:
            squad_df["common_position"] = (
                squad_df[position_col]
                .map(self.POSITION_TO_ROLE)
                .fillna(squad_df[position_col])
            )

        if current_team_col in squad_df.columns and original_team_col in squad_df.columns:
            team_current = (
                squad_df[current_team_col]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            team_original = (
                squad_df[original_team_col]
                .fillna("")
                .astype(str)
                .str.strip()
            )
            
            loan_status = (
                squad_df["on_loan"]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.strip()
            )

            same_team = team_original.str.lower().eq(team_current.str.lower())
            squad_df["on_loan"] = np.where(
                loan_status.eq("yes") & same_team,
                "✅",
                np.where(
                    loan_status.eq("yes"),
                    "✅ - @ " + team_original,
                    "-",
                ),
            )
        else:
            squad_df["on_loan"] = "-"

        return squad_df
    
    def build_league_season_df_from_player(
        self,
        player_row: pd.Series,
        league_col: str = "league_name",
        season_col: str = "season",
    ) -> pd.DataFrame:
        wyscout_df = self.prepare_wyscout_data().copy()

        league_name = player_row.get(league_col)
        # season = player_row.get(season_col)

        # if pd.isna(league_name) or pd.isna(season):
        #     return pd.DataFrame()

        league_season_df = (
            wyscout_df[
                (wyscout_df[league_col].astype(str).eq(str(league_name)))
                # & (wyscout_df[season_col].astype(str).eq(str(season)))
            ]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        return league_season_df
    
    def build_player_df(
        self,
        player: str,
        team: str,
        # season: str,
    ) -> pd.DataFrame:
        wyscout_df = self.prepare_wyscout_data().copy()

        # wyscout_df["player_slug"] = wyscout_df["player"].apply(self.slugify)
        # wyscout_df["team_slug"] = wyscout_df["team_within_selected_timeframe"].apply(self.slugify)
        # wyscout_df["season_slug"] = wyscout_df["season"].apply(self.slugify)

        player_df = (
            wyscout_df[
                (wyscout_df["player_slug"] == player)
                & (wyscout_df["team_slug"] == team)
                # & (wyscout_df["season_slug"] == season)
            ]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        if player_df.empty:
            return player_df

        # player_df["common_position"] = (
        #     player_df["position"]
        #     .map(self.POSITION_TO_ROLE)
        #     .fillna(player_df["position"])
        # )

        team_current = (
            player_df["team_within_selected_timeframe"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        team_original = (
            player_df["team"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        loan_status = (
            player_df["on_loan"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.strip()
        )

        same_team = team_original.str.lower().eq(team_current.str.lower())

        player_df["on_loan"] = np.where(
            loan_status.eq("yes") & same_team,
            "✅",
            np.where(
                loan_status.eq("yes"),
                "✅ - @ " + team_original,
                "-",
            ),
        )

        return player_df
    
    def slugify(self, value: str) -> str:
        value = str(value).lower().strip()
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-")