# =================
# BRAND COLORS
# =================
BRAND_COLORS = {
    "background_main": "#0F172A",
    "background_panel": "#1E293B",
    "background_soft": "#334155",
    "text_main": "#E2E8F0",
    "text_body": "#CBD5E1",
    "text_muted": "#94A3B8",
    "border": "#475569",
}

# =================
# CHART COLORS
# =================
# Full chart palette used across the project.
# This keeps all tactical group colors centralized in one place.
CHART_COLORS = {
    "amber": "#F59E0B",
    "orange": "#FB923C",
    "red": "#F87171",
    "rose": "#FB7185",
    "coral": "#FF6B6B",

    "cyan": "#22D3EE",
    "teal": "#2DD4BF",
    "emerald": "#34D399",
    "green": "#86EFAC",
    "lime": "#A3E635",

    "violet": "#A78BFA",
    "purple": "#C084FC",
    "fuchsia": "#E879F9",
    "pink": "#F472B6",
    "sky": "#7DD3FC",

    "yellow": "#FDE047",
    "gold": "#FBBF24",
    "salmon": "#FDA4AF",
    "magenta": "#DB2777",

    "slate": "#94A3B8",
    "stone": "#A8A29E",
    "zinc": "#A1A1AA",
    "mint": "#5EEAD4",
    "apricot": "#FDBA74",

    "lavender": "#C4B5FD",
    "turquoise": "#14B8A6",
    "peach": "#FED7AA",
    "light_red": "#FCA5A5",
    "light_cyan": "#A5F3FC",
    "light_green": "#BBF7D0",

    "electric_purple": "#D946EF",
    "bright_green": "#22C55E",
    "warm_yellow": "#EAB308",
    "hot_pink": "#EC4899",
}

# =================
# GROUP COLORS
# =================
# Every tactical group now uses only colors defined in CHART_COLORS.
GROUP_COLORS = {
    "Shot Stopping": CHART_COLORS["sky"],
    "Area Control": CHART_COLORS["mint"],

    "Defending": CHART_COLORS["emerald"],
    "Duel Winning": CHART_COLORS["orange"],
    "Duels": CHART_COLORS["rose"],
    "Defensive Duels": CHART_COLORS["rose"],
    "Defensive Contribution": CHART_COLORS["coral"],
    "Box Defending": CHART_COLORS["lime"],

    "Aerial Dominance": CHART_COLORS["red"],
    "Aerial Ability": CHART_COLORS["red"],

    "Distribution": CHART_COLORS["violet"],
    "Ball Retention": CHART_COLORS["purple"],
    "Passing": CHART_COLORS["lavender"],
    "Press Resistance": CHART_COLORS["fuchsia"],
    "Receiving": CHART_COLORS["pink"],
    "Receiving & Possession": CHART_COLORS["salmon"],
    "Link-Up Play": CHART_COLORS["emerald"],

    "Progression": CHART_COLORS["cyan"],
    "Basic Progression": CHART_COLORS["cyan"],
    "Passing Progression": CHART_COLORS["cyan"],
    "Ball Carrying": CHART_COLORS["light_red"],
    "Forward Release": CHART_COLORS["yellow"],
    "Long Distribution": CHART_COLORS["magenta"],
    "Mobility": CHART_COLORS["green"],
    "Movement": CHART_COLORS["lime"],

    "Crossing": CHART_COLORS["gold"],
    "Creativity": CHART_COLORS["yellow"],

    "Chance Creation": CHART_COLORS["magenta"],
    "Final Third Presence": CHART_COLORS["magenta"],
    "Final Third Output": CHART_COLORS["light_red"],
    "Final Third Involvement": CHART_COLORS["peach"],
    "Involvement": CHART_COLORS["peach"],
    "Attacking Involvement": CHART_COLORS["peach"],

    "Goal Threat": CHART_COLORS["light_green"],
    "Box Threat": CHART_COLORS["gold"],
    "Finishing": CHART_COLORS["sky"],

    "Dribbling": CHART_COLORS["electric_purple"],
    "1v1 Ability": CHART_COLORS["slate"],

    "Depth Threat": CHART_COLORS["salmon"],
    "Reference Play": CHART_COLORS["mint"],
}