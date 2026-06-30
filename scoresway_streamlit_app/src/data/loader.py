# =========================
# DATA LOADER
# =========================

from pathlib import Path
import re

import pandas as pd

from src.config.leagues import LEAGUE_FILE_METADATA


def parse_team_stats_filename(file_path: Path) -> dict:
    """
    Extract league slug and season from a processed team stats file.

    Expected format:
    england_premier_league_2025_26_team_stats.csv
    """

    file_name = file_path.name
    stem = file_name.replace("_team_stats.csv", "")

    season_match = re.search(r"_(\d{4})_(\d{2})$", stem)

    if season_match is None:
        return {
            "source_league_slug": stem,
            "source_season": None,
        }

    season_start = season_match.group(1)
    season_end = season_match.group(2)

    league_slug = stem[: season_match.start()]
    season = f"{season_start}-{season_end}"

    return {
        "source_league_slug": league_slug,
        "source_season": season,
    }


def get_file_metadata(file_path: Path) -> dict:
    """
    Build metadata columns from file name and static config.
    """

    parsed = parse_team_stats_filename(file_path)

    league_slug = parsed["source_league_slug"]
    league_metadata = LEAGUE_FILE_METADATA.get(league_slug, {})

    return {
        "source_file": str(file_path),
        "source_league_slug": league_slug,
        "source_country_name": league_metadata.get("country_name", "Unknown"),
        "source_league_name": league_metadata.get("league_name", league_slug),
        "source_season": parsed["source_season"],
    }


def load_team_stats_files(
    data_dir: str | Path = "data/processed",
) -> pd.DataFrame:
    """
    Load all processed Scoresway team stats CSV files.
    """

    data_dir = Path(data_dir)

    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    files = sorted(data_dir.glob("*_team_stats.csv"))

    if not files:
        raise FileNotFoundError(
            f"No team stats CSV files found in: {data_dir}"
        )

    frames = []

    for file_path in files:
        df = pd.read_csv(file_path)

        metadata = get_file_metadata(file_path)

        for col, value in metadata.items():
            df[col] = value

        frames.append(df)

    return pd.concat(frames, ignore_index=True)