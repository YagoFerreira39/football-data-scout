# =========================
# VISUAL THEME
# =========================

from matplotlib import font_manager


def get_report_font_family() -> str:
    """
    Uses Space Grotesk if available.
    Falls back safely if the font is not installed.
    """

    available_fonts = {
        font.name for font in font_manager.fontManager.ttflist
    }

    if "Space Grotesk" in available_fonts:
        return "Space Grotesk"

    return "DejaVu Sans"


APP_THEME = {
    # App / report base
    "background": "#0F172A",
    "surface": "#111827",
    "surface_alt": "#162033",

    # Text
    "text": "#E5E7EB",
    "muted_text": "#AEB9CC",
    "subtle_text": "#CBD5E1",

    # Lines / grid
    "grid": "#31476E",
    "line": "#31476E",

    # Markers
    "selected_team": "#F59E0B",
    "league_average": "#F8FAFC",
    "league_distribution": "#AEB9CC",

    # Accents
    "positive": "#86EFAC",
    "warning": "#FBBF24",
    "negative": "#FCA5A5",

    # Font
    "font_family": get_report_font_family(),
}