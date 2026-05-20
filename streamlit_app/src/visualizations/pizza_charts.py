import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mplsoccer import PyPizza
from scipy.stats import rankdata

from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
import matplotlib.patheffects as patheffects
import matplotlib.colors as mc

import colorsys

# =================
# GLOBAL FONT SIZE
# =================
from pathlib import Path


plt.rcParams["font.size"] = 11


# =================
# FONT CONFIGURATION
# =================
# Font used in regular text
font_normal = FontProperties(family="DejaVu Sans", size=11)

# Font used in chart titles
font_bold = FontProperties(family="DejaVu Sans", weight="bold", size=14)


# =================
# FEATURE GROUPS BY ROLE
# =================
# Each role has its own grouped metrics.
# These groups are used to:
# 1. define which features appear in the pizza chart
# 2. assign colors by tactical category
FEATURE_GROUPS_BY_ROLE = {
    "GK_default": {
        "Shot Stopping": [
            "save_rate_%",
            "prevented_goals_per_90",
            "conceded_goals_per_90",
            "clean_sheets",
            "shots_against_per_90",
        ],
        "Area Control": [
            "exits_per_90",
            "aerial_duels_per_90.1",
        ],
        "Distribution": [
            "passes_per_90",
            "accurate_passes_%",
            "long_passes_per_90",
            "accurate_long_passes_%",
            "average_long_pass_length_m",
        ],
    },
    # CB 
    "CB_default": {
        "Defending": [
            "defensive_duels_won_%",
            "defensive_duels_per_90",
            "padj_interceptions",
            "padj_sliding_tackles",
        ],

        "Aerial Ability": [
            "aerial_duels_won_%",
            "aerial_duels_per_90",
        ],
        
        "Box Defending": [
          "shots_blocked_per_90",
          "interceptions_per_90",  
        ],

        "Ball Retention": [
            "accurate_passes_%",
            "accurate_short_/_medium_passes_%",
            "passes_per_90",
        ],

        "Basic Progression": [
            "forward_passes_per_90",
            "accurate_forward_passes_%",
            "long_passes_per_90",
        ]
    },
    "CB_aerially_dominant": {
        "Defending": [
            "defensive_duels_per_90",
            "defensive_duels_won_%",
            "interceptions_per_90",
            "shots_blocked_per_90",
        ],

        "Aerial Dominance": [
            "aerial_duels_per_90",
            "aerial_duels_won_%",
            "head_goals_per_90",
        ],

        "Progression": [
            "progressive_passes_per_90",
            "passes_to_final_third_per_90",
            "long_passes_per_90",
            "accurate_long_passes_%",
        ],

        "Ball Retention": [
            "passes_per_90",
            "accurate_passes_%",
            "forward_passes_per_90",
            "accurate_forward_passes_%",
        ],
    },
    "CB_ball_playing": {
        "Passing Progression": [
            "progressive_passes_per_90",
            "accurate_progressive_passes_%",
            "passes_to_final_third_per_90",
            "accurate_passes_to_final_third_%",
        ],

        "Defending": [
            "defensive_duels_won_%",
            "defensive_duels_per_90",
            "padj_interceptions",
            "padj_sliding_tackles",
        ],

        "Ball Carrying": [
            "progressive_runs_per_90",
            "accelerations_per_90",
        ],

        "Ball Retention": [
            "accurate_passes_%",
            "accurate_short_/_medium_passes_%",
            "short_/_medium_passes_per_90",
            "fouls_suffered_per_90",
        ],

        "Long Distribution": [
            "accurate_long_passes_%",
            "long_passes_per_90",
            "forward_passes_per_90",
            "accurate_forward_passes_%",
        ],

        "Aerial Ability": [
            "aerial_duels_won_%",
            "aerial_duels_per_90",
        ],
    },
    # Full-Backs
    "FB_default": {
        "Defending": [
            "padj_interceptions",
            "interceptions_per_90",
            "padj_sliding_tackles",
        ],

        "Defensive Duels": [
            "defensive_duels_per_90",
            "defensive_duels_won_%",
            "aerial_duels_won_%",
            "aerial_duels_per_90",
        ],

        "Crossing": [
            "crosses_per_90",
            "accurate_crosses_%",
        ],

        "Ball Retention": [
            "accurate_passes_%",
            "passes_per_90",
        ],

        "Progression": [
            "progressive_passes_per_90",
            "progressive_runs_per_90",
            "passes_to_final_third_per_90",
        ],
    },
    "FB_defensive_fullback": {
        "Defending": [
            "padj_interceptions",
            "interceptions_per_90",
            "padj_sliding_tackles",
        ],

        "Duel Winning": [
            "defensive_duels_per_90",
            "defensive_duels_won_%",
            "aerial_duels_won_%",
        ],

        "Ball Retention": [
            "accurate_passes_%",
            "accurate_short_/_medium_passes_%",
            "passes_per_90",
        ],

        "Progression": [
            "forward_passes_per_90",
            "accurate_forward_passes_%",
            "long_passes_per_90",
            "accurate_long_passes_%",
        ],
    },
    "FB_attacking_fullback": {
        "Crossing": [
            "accurate_crosses_%",
            "crosses_per_90",
        ],

        "Dribbling": [
            "dribbles_per_90",
            "successful_dribbles_%",
            # "offensive_duels_won_%",
        ],

        "Defending": [
            "defensive_duels_won_%",
            "defensive_duels_per_90",
            "padj_interceptions",
        ],

        "Progression": [
            "progressive_runs_per_90",           
            "progressive_passes_per_90",
            "accurate_progressive_passes_%",
            "accurate_passes_to_final_third_%",
            # "accurate_short_/_medium_passes_%",
            # "passes_to_final_third_per_90", 
        ],

        "Chance Creation": [
            "xa_per_90",
            "key_passes_per_90",
            "assists_per_90",
        ],
    },
    "FB_inverted_fullback": {
        "Involvement": [
            "received_passes_per_90",
            "passes_per_90",
            "short_/_medium_passes_per_90",
        ],

        "Passing Progression": [
            "progressive_passes_per_90",
            "accurate_progressive_passes_%",
            "passes_to_final_third_per_90",
        ],

        "Ball Retention": [
            "accurate_passes_%",
            "accurate_short_/_medium_passes_%",
            "fouls_suffered_per_90",
        ],

        "Defending": [
            "padj_interceptions",
            "defensive_duels_per_90",
            "defensive_duels_won_%",
        ],

        "Mobility": [
            "progressive_runs_per_90",
            "accelerations_per_90",
        ],
    },
    "WB_wing_back": {
        "Crossing": [
            "accurate_crosses_%",
            "crosses_per_90",
        ],

        "Chance Creation": [
            "xa_per_90",
            "key_passes_per_90",
            "passes_to_penalty_area_per_90",
            "accurate_passes_to_penalty_area_%",
        ],

        "Progression": [
            "progressive_runs_per_90",
            "progressive_passes_per_90",
            "passes_to_final_third_per_90",
        ],

        "Dribbling": [
            "dribbles_per_90",
            "successful_dribbles_%",
            "offensive_duels_won_%",
        ],

        "Attacking Threat": [
            "non_penalty_xg_per_90",
            "touches_in_box_per_90",
            "shots_on_target_%",
        ],

        "Defensive Duels": [
            "defensive_duels_won_%",
            "defensive_duels_per_90",
            "aerial_duels_won_%",
            "aerial_duels_per_90",
        ],

        "Proactive Defending": [
            "interceptions_per_90",
            "padj_interceptions",
            "padj_sliding_tackles",
        ],
    },
    
    "DM_default": {
        "Defending": [
            "padj_interceptions",
            "padj_sliding_tackles",
            "defensive_duels_per_90",
            "defensive_duels_won_%",
        ],

        "Aerial Ability": [
            "aerial_duels_won_%",
            "aerial_duels_per_90",
        ],

        "Ball Retention": [
            "passes_per_90",
            "accurate_passes_%",
            # "accurate_short_/_medium_passes_%",
        ],

        "Passing Progression": [
            "passes_to_final_third_per_90",
            "progressive_passes_per_90",
            "accurate_progressive_passes_%",
        ],

        "Ball Carrying": [
            "progressive_runs_per_90",
            "accelerations_per_90",
            "received_passes_per_90",
        ],
    },
    
    # "CM_default": {
    #     "Defending": [
    #         "padj_interceptions",
    #         "padj_sliding_tackles",
    #         "defensive_duels_per_90",
    #         "defensive_duels_won_%",
    #     ],

    #     "Aerial Ability": [
    #         "aerial_duels_won_%",
    #         "aerial_duels_per_90",
    #     ],

    #     "Ball Retention": [
    #         "passes_per_90",
    #         "accurate_passes_%",
    #     ],

    #     "Distribution": [
    #         "long_passes_per_90",
    #         "accurate_long_passes_%",
    #         "short_/_medium_passes_per_90",
    #     ],

    #     "Passing Progression": [
    #         "progressive_passes_per_90",
    #         "passes_to_final_third_per_90",
    #         "accurate_progressive_passes_%",
    #     ],

    #     "Ball Carrying": [
    #         "progressive_runs_per_90",
    #         "accelerations_per_90",
    #         "received_passes_per_90",
    #     ],
    # },
    
    "DM_ball_playing_midfielder": {
        "Distribution": [
            "passes_per_90",
            "accurate_passes_%",
            "short_/_medium_passes_per_90",
            "accurate_short_/_medium_passes_%",
        ],

        "Progression": [
            "progressive_passes_per_90",
            "accurate_progressive_passes_%",
            "passes_to_final_third_per_90",
            "accurate_passes_to_final_third_%",
        ],

        "Defending": [
            "padj_interceptions",
            "padj_sliding_tackles",
            "defensive_duels_per_90",
            "defensive_duels_won_%",
        ],

        "Press Resistance": [
            "received_passes_per_90",
            "fouls_suffered_per_90",
        ],

        "Ball Carrying": [
            "dribbles_per_90",
            "successful_dribbles_%",
            "progressive_runs_per_90",
        ],

        "Long Distribution": [
            "long_passes_per_90",
            "accurate_long_passes_%",
            "forward_passes_per_90",
            "accurate_forward_passes_%",
        ],
    },
    "CM_ball_playing_midfielder": {
        "Distribution": [
            "passes_per_90",
            "accurate_passes_%",
            "short_/_medium_passes_per_90",
            "accurate_short_/_medium_passes_%",
        ],

        "Progression": [
            "progressive_passes_per_90",
            "accurate_progressive_passes_%",
            "passes_to_final_third_per_90",
            "accurate_passes_to_final_third_%",
        ],

        "Defending": [
            "padj_interceptions",
            "padj_sliding_tackles",
            "defensive_duels_per_90",
            "defensive_duels_won_%",
        ],

        "Press Resistance": [
            "received_passes_per_90",
            "fouls_suffered_per_90",
        ],

        "Ball Carrying": [
            "dribbles_per_90",
            "successful_dribbles_%",
            "progressive_runs_per_90",
        ],

        "Long Distribution": [
            "long_passes_per_90",
            "accurate_long_passes_%",
            "forward_passes_per_90",
            "accurate_forward_passes_%",
        ],
    },
    "DM_ball_winning_midfielder": {
        "Defending": [
            "padj_interceptions",
            "interceptions_per_90",
            "successful_defensive_actions_per_90",
            "shots_blocked_per_90",
        ],

        "Duel Winning": [
            "defensive_duels_per_90",
            "defensive_duels_won_%",
            "padj_sliding_tackles",
            "aerial_duels_per_90",
            "aerial_duels_won_%",
        ],

        "Ball Retention": [
            "passes_per_90",
            "accurate_passes_%",
            "short_/_medium_passes_per_90",
            "accurate_short_/_medium_passes_%",
        ],

        "Forward Release": [
            "forward_passes_per_90",
            "accurate_forward_passes_%",
            "progressive_passes_per_90",
            "accurate_progressive_passes_%",
            "long_passes_per_90",
            "accurate_long_passes_%",
        ],
    },
    "CM_ball_winning_midfielder": {
        "Defending": [
            "padj_interceptions",
            "interceptions_per_90",
            "successful_defensive_actions_per_90",
            "shots_blocked_per_90",
        ],

        "Duel Winning": [
            "defensive_duels_per_90",
            "defensive_duels_won_%",
            "padj_sliding_tackles",
            "aerial_duels_per_90",
            "aerial_duels_won_%",
        ],

        "Ball Retention": [
            "passes_per_90",
            "accurate_passes_%",
            "short_/_medium_passes_per_90",
            "accurate_short_/_medium_passes_%",
        ],

        "Forward Release": [
            "forward_passes_per_90",
            "accurate_forward_passes_%",
            "progressive_passes_per_90",
            "accurate_progressive_passes_%",
            "long_passes_per_90",
            "accurate_long_passes_%",
        ],
    },
    "DM_box_to_box": {
        "Defending": [
            "defensive_duels_per_90",
            "defensive_duels_won_%",
            "padj_interceptions",
            "padj_sliding_tackles",
        ],

        "Ball Carrying": [
            "progressive_runs_per_90",
            "accelerations_per_90",
            "received_passes_per_90",
        ],

        "Passing Progression": [
            "progressive_passes_per_90",
            "passes_to_final_third_per_90",
            "accurate_progressive_passes_%",
            "accurate_passes_to_final_third_%",
        ],

        "Ball Retention": [
            "passes_per_90",
            "accurate_passes_%",
        ],

        "Chance Creation": [
            "xa_per_90",
            "key_passes_per_90",
            "shot_assists_per_90",
        ],

        "Box Threat": [
            "touches_in_box_per_90",
            "non_penalty_xg_per_90",
            "shots_per_90",
            "non-penalty_goals_per_90",
        ],
    },
    
    "CM_box_to_box": {
        "Defending": [
            "defensive_duels_per_90",
            "defensive_duels_won_%",
            "padj_interceptions",
            "padj_sliding_tackles",
        ],

        "Ball Carrying": [
            "progressive_runs_per_90",
            "accelerations_per_90",
            "received_passes_per_90",
        ],

        "Passing Progression": [
            "progressive_passes_per_90",
            "passes_to_final_third_per_90",
            "accurate_progressive_passes_%",
            "accurate_passes_to_final_third_%",
        ],

        "Ball Retention": [
            "passes_per_90",
            "accurate_passes_%",
        ],

        "Chance Creation": [
            "xa_per_90",
            "key_passes_per_90",
            "shot_assists_per_90",
        ],

        "Box Threat": [
            "touches_in_box_per_90",
            "non_penalty_xg_per_90",
            "shots_per_90",
            "non-penalty_goals_per_90",
        ],
    },
    
    "AM_default": {
        "Chance Creation": [
            "xa_per_100_passes",
            "key_passes_per_100_passes",
        ],

        "Goal Threat": [
            "non_penalty_xg_per_90",
            "non-penalty_goals_per_90",
            "shots_per_90",
            "shots_on_target_%",
        ],

        "Passing": [
            "passes_per_90",
            "accurate_passes_%",
            "through_passes_per_90",
        ],

        "Dribbling": [
            "dribbles_per_90",
            "successful_dribbles_%",
        ],
    },
    
    "AM_attacking_midfielder": {
        "Chance Creation": [
            "xa_per_100_passes",
            "key_passes_per_100_passes",
            "smart_passes_per_90",
        ],

        "Goal Threat": [
            "non_penalty_xg_per_90",
            "shots_per_90",
            "non-penalty_goals_per_90",
            "shots_on_target_%",
        ],

        "Receiving": [
            "received_passes_per_90",
            "fouls_suffered_per_90",
            "touches_in_box_per_90",
        ],

        "Passing": [
            "passes_per_90",
            "accurate_passes_%",
            "short_/_medium_passes_per_90",
            "through_passes_per_90",
        ],

        "Dribbling": [
            "dribbles_per_90",
            "successful_dribbles_%",
        ],
    },
    
    "WINGER_default": {
        "Dribbling": [
            "dribbles_per_90",
            "successful_dribbles_%",
            "offensive_duels_won_%",
        ],

        "Chance Creation": [
            "xa_per_90",
            "key_passes_per_90",
        ],

        "Defensive Contribution": [
            "defensive_duels_per_90",
            "defensive_duels_won_%",
        ],
        
        "Attacking Involvement": [
            "successful_attacking_actions_per_90",
            "offensive_duels_per_90",
            "received_passes_per_90",
        ],

        "Goal Threat": [
            "non_penalty_xg_per_90",
            "shots_per_90",
            "goal_conversion_%",
        ],

        "Crossing": [
            "crosses_per_90",
            "accurate_crosses_%",
        ],

    },
    
    "WINGER_touchline_winger": {
        "Dribbling": [
            "dribbles_per_90",
            "successful_dribbles_%",
            "offensive_duels_won_%",
            "offensive_duels_per_90",
        ],

        "Chance Creation": [
            "xa_per_90",
            "key_passes_per_90",
            "passes_to_penalty_area_per_90",
            "accurate_passes_to_penalty_area_%",
        ],

        "Progression": [
            "progressive_runs_per_90",
            "accelerations_per_90",
            "progressive_passes_per_90",
            "passes_to_final_third_per_90",
        ],

        "Defensive Contribution": [
            "defensive_duels_per_90",
            "defensive_duels_won_%",
        ],

        "Ball Retention": [
            "received_passes_per_90",
            "accurate_short_/_medium_passes_%",
            "accurate_passes_%",
        ],

        "Crossing": [
            "accurate_crosses_%",
            "crosses_per_90",
            "deep_completed_crosses_per_90",
        ],
    },
    
    "WINGER_half_space_drifter": {
        "Chance Creation": [
            "xa_per_90",
            "key_passes_per_90",
            "smart_passes_per_90",
        ],

        "Goal Threat": [
            "non_penalty_xg_per_90",
            "shots_per_90",
            "touches_in_box_per_90",
            "shots_on_target_%",
        ],

        "Dribbling": [
            "dribbles_per_90",
            "successful_dribbles_%",
            "progressive_runs_per_90",
            "accelerations_per_90",
        ],

        "Passing": [
            "passes_per_90",
            "accurate_passes_%",
            "short_/_medium_passes_per_90",
            "accurate_short_/_medium_passes_%",
        ],

        "Passing Progression": [
            "progressive_passes_per_90",
            "passes_to_final_third_per_90",
            "through_passes_per_90",
            "accurate_progressive_passes_%",
        ],

        "Crossing": [
            "crosses_per_90",
            "accurate_crosses_%",
        ],
    },
    
    "WINGER_inside_forward_winger": {
        "Box Threat": [
            "non_penalty_xg_per_90",
            "non-penalty_goals_per_90",
            "touches_in_box_per_90",
            "received_passes_per_90",
        ],

        "Final Third Output": [
            "shots_per_90",
            "shots_on_target_%",
            "goal_conversion_%",
            "xa_per_90",
            "key_passes_per_90",
        ],

        "Ball Carrying": [
            "progressive_runs_per_90",
            "dribbles_per_90",
            "successful_dribbles_%",
            "offensive_duels_won_%",
            "accelerations_per_90",
        ],

        "Attacking Involvement": [
            "successful_attacking_actions_per_90",
            "passes_to_penalty_area_per_90",
            "offensive_duels_per_90",
        ],
    },

    "CF_mobile_run_behind": {
        "Box Threat": [
            "non_penalty_xg_per_90",
            "touches_in_box_per_90",
            "shots_per_90",
        ],

        "Finishing": [
            "non-penalty_goals_per_90",
            "shots_on_target_%",
            "goal_conversion_%",
        ],

        "Depth Threat": [
            "received_long_passes_per_90",
            "accelerations_per_90",
            "received_passes_per_90",
        ],

        "Ball Carrying": [
            "progressive_runs_per_90",
            "dribbles_per_90",
            "successful_dribbles_%",
            "offensive_duels_won_%",
        ],
    },
    
    "CF_default": {
        "Box Threat": [
            "non_penalty_xg_per_90",
            "touches_in_box_per_90",
            "shots_per_90",
        ],

        "Finishing": [
            "non-penalty_goals_per_90",
            "shots_on_target_%",
            "goal_conversion_%",
        ],

        "Link-Up Play": [
            "received_passes_per_90",
            "short_/_medium_passes_per_90",
            "shot_assists_per_90",
        ],

        "Aerial Ability": [
            "aerial_duels_per_90",
            "aerial_duels_won_%",
        ],
    },
        
    "CF_target_man": {
        "Reference Play": [
            "received_long_passes_per_90",
            "offensive_duels_per_90",
            "offensive_duels_won_%",
        ],

        "Aerial Dominance": [
            "aerial_duels_per_90",
            "aerial_duels_won_%",
        ],

        "Box Threat": [
            "non_penalty_xg_per_90",
            "non-penalty_goals_per_90",
            "shots_per_90",
            "shots_on_target_%",
        ],

        "Link-Up Play": [
            "received_passes_per_90",
            "short_/_medium_passes_per_90",
            "accurate_short_/_medium_passes_%",
            "shot_assists_per_90",
        ],
    },

}


# =================
# POSITION TO ROLE MAP
# =================
# Maps detailed positions to broader roles
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

    "LCMF": "CM",
    "RCMF": "CM",

    "AMF": "AM",
    # "LAMF": "AM",
    # "RAMF": "AM",

    
    "LAMF": "WINGER",
    "RAMF": "WINGER",
    "LW": "WINGER",
    "RW": "WINGER",
    "LWF": "WINGER",
    "RWF": "WINGER",

    "CF": "CF",
}

COMPARISON_GROUPS = {
    "GK": ["GK"],
    "CB": ["CB", "CCB", "LCB", "RCB"],
    "LB_LWB": ["LB", "LWB"],
    "RB_RWB": ["RB", "RWB"],
    "DM": ["DMF", "LDMF", "RDMF"],
    "CM": ["LCMF", "RCMF"],
    "AM": ["AMF"],
    # "AM": ["AMF", "LAMF", "RAMF"],
    "LWF": ["LW", "LWF", "LAMF"],
    "RWF": ["RW", "RWF", "RAMF"],
    "CF": ["CF"],
}

POSITION_TO_COMPARISON_GROUP = {
    position: group_name
    for group_name, positions in COMPARISON_GROUPS.items()
    for position in positions
}

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
    "Receiving": CHART_COLORS["salmon"],
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

    "Dribbling": CHART_COLORS["peach"],
    "1v1 Ability": CHART_COLORS["slate"],

    "Depth Threat": CHART_COLORS["salmon"],
    "Reference Play": CHART_COLORS["mint"],
}


# =================
# FEATURE LABELS
# =================
# Human-readable labels shown around the pizza chart
# FEATURE_LABELS = {
#     # =================
#     # General / Metadata
#     # =================
#     "matches_played": "Matches",
#     "minutes_played": "Minutes",
#     "age": "Age",
#     "height": "Height",
#     "weight": "Weight",
#     "market_value": "Market Value",

#     # =================
#     # Shooting / Box Threat
#     # =================
#     "goals": "Goals",
#     "goals_per_90": "Goals/90",
#     "xg": "xG",
#     "xg_per_90": "xG/90",
#     "shots": "Shots",
#     "shots_per_90": "Shots Volume",
#     "shots_on_target_%": "Shot Accuracy",
#     "goal_conversion_%": "Shot Conversion",
#     "non-penalty_goals": "nP Goals",
#     "non-penalty_goals_per_90": "nP Goals/90",
#     "non_penalty_xg": "nP xG",
#     "non_penalty_xg_per_90": "nP xG/90",
#     "touches_in_box_per_90": "Box Touches",
#     "head_goals": "Head Goals",
#     "head_goals_per_90": "Head Goals/90",
#     "penalties_taken": "Penalties Taken",
#     "penalty_conversion_%": "Penalty Conversion",

#     # =================
#     # Creativity / Chance Creation
#     # =================
#     "assists": "Assists",
#     "assists_per_90": "Assists/90",
#     "xa": "xA",
#     "xa_per_90": "xA/90",
#     "xa_per_100_passes": "xA/100 Passes",
#     "shot_assists_per_90": "Shot Assists",
#     "key_passes_per_90": "Key Passes",
#     "key_passes_per_100_passes": "Key Passes/100 Passes",
#     "smart_passes_per_90": "Smart Passes",
#     "accurate_smart_passes_%": "Smart Pass Accuracy",
#     "through_passes_per_90": "Through Passes",
#     "accurate_through_passes_%": "Through Pass Accuracy",
#     "second_assists_per_90": "Second Assists",
#     "third_assists_per_90": "Third Assists",

#     # =================
#     # General Passing / Distribution
#     # =================
#     "passes_per_90": "Passing Volume",
#     "accurate_passes_%": "Pass Accuracy",
#     "forward_passes_per_90": "Forward Passes",
#     "accurate_forward_passes_%": "Forward Pass Accuracy",
#     "back_passes_per_90": "Back Passes",
#     "accurate_back_passes_%": "Back Pass Accuracy",
#     "lateral_passes_per_90": "Lateral Passes",
#     "accurate_lateral_passes_%": "Lateral Pass Accuracy",
#     "short_/_medium_passes_per_90": "Short/Medium Passes",
#     "accurate_short_/_medium_passes_%": "Short/Medium Pass Accuracy",
#     "received_passes_per_90": "Ball Reception",
#     "received_long_passes_per_90": "Long Ball Reception",
#     "average_pass_length_m": "Avg Pass Length",

#     # =================
#     # Progression / Penetration
#     # =================
#     "progressive_passes_per_90": "Progressive Passes",
#     "accurate_progressive_passes_%": "Progressive Pass Accuracy",
#     "progressive_runs_per_90": "Progressive Runs",
#     "passes_to_final_third_per_90": "Final 3rd Passes",
#     "accurate_passes_to_final_third_%": "Final 3rd Pass Accuracy",
#     "passes_to_penalty_area_per_90": "Penalty Area Passes",
#     "accurate_passes_to_penalty_area_%": "Penalty Area Pass Accuracy",
#     "deep_completions_per_90": "Deep Completions",

#     # =================
#     # Long Passing
#     # =================
#     "long_passes_per_90": "Long Passes",
#     "accurate_long_passes_%": "Long Pass Accuracy",
#     "average_long_pass_length_m": "Long Pass Length",

#     # =================
#     # Crossing / Delivery
#     # =================
#     "crosses_per_90": "Crosses",
#     "accurate_crosses_%": "Cross Accuracy",
#     "crosses_from_left_flank_per_90": "Left Flank Crosses",
#     "accurate_crosses_from_left_flank_%": "Left Cross Accuracy",
#     "crosses_from_right_flank_per_90": "Right Flank Crosses",
#     "accurate_crosses_from_right_flank_%": "Right Cross Accuracy",
#     "crosses_to_goalie_box_per_90": "Goal Box Crosses",
#     "deep_completed_crosses_per_90": "Deep Crosses",

#     # =================
#     # Dribbling / 1v1 Ability
#     # =================
#     "dribbles_per_90": "Dribbles",
#     "successful_dribbles_%": "Dribble Success",
#     "offensive_duels_per_90": "Off. Duels",
#     "offensive_duels_won_%": "Off. Duel Win %",
#     "successful_attacking_actions_per_90": "Successful Att. Actions",
#     "fouls_suffered_per_90": "Fouls Suffered",
#     "accelerations_per_90": "Accelerations",

#     # =================
#     # Duels / Physical Contest
#     # =================
#     "duels_per_90": "Total Duels",
#     "duels_won_%": "Total Duel Win %",

#     # =================
#     # Defending / Discipline
#     # =================
#     "successful_defensive_actions_per_90": "Defensive Actions",
#     "defensive_duels_per_90": "Defensive Duels",
#     "defensive_duels_won_%": "Def. Duel Win %",
#     "interceptions_per_90": "Interceptions",
#     "padj_interceptions": "Adj. Interceptions",
#     "p_adj_interceptions": "Adj. Interceptions",
#     "shots_blocked_per_90": "Shots Blocked",
#     "sliding_tackles_per_90": "Sliding Tackles",
#     "padj_sliding_tackles": "Adj. Sliding Tackles",
#     "p_adj_sliding_tackles": "Adj. Sliding Tackles",
#     "fouls_per_90": "Fouls Committed",
#     "yellow_cards": "Yellow Cards",
#     "yellow_cards_per_90": "Yellow Cards/90",
#     "red_cards": "Red Cards",
#     "red_cards_per_90": "Red Cards/90",

#     # =================
#     # Aerial Ability
#     # =================
#     "aerial_duels_per_90": "Aerial Duels",
#     "aerial_duels_won_%": "Aerial Win %",

#     # =================
#     # Set Pieces
#     # =================
#     "free_kicks_per_90": "Free Kicks",
#     "direct_free_kicks_per_90": "Direct Free Kicks",
#     "direct_free_kicks_on_target_%": "Direct FK Accuracy",
#     "corners_per_90": "Corners",

#     # =================
#     # Goalkeeper
#     # =================
#     "conceded_goals": "Goals Conceded",
#     "conceded_goals_per_90": "Goals Conceded/90",
#     "shots_against": "Shots Against",
#     "shots_against_per_90": "Shots Against/90",
#     "clean_sheets": "Clean Sheets",
#     "save_rate_%": "Save Rate",
#     "xg_against": "xG Against",
#     "xg_against_per_90": "xG Against/90",
#     "prevented_goals": "Prevented Goals",
#     "prevented_goals_per_90": "Prevented Goals/90",
#     "back_passes_received_as_gk_per_90": "GK Back Passes Received",
#     "exits_per_90": "Exits",
#     "aerial_duels_per_90.1": "GK Aerial Duels",
#     "aerial_duels_per_90_1": "GK Aerial Duels",
# }

FEATURE_LABELS = {
    # =================
    # General / Metadata
    # =================
    "matches_played": "Matches Played",
    "minutes_played": "Minutes Played",
    "age": "Age",
    "height": "Height",
    "weight": "Weight",
    "market_value": "Market Value",

    # =================
    # Shooting / Box Threat
    # =================
    "goals": "Goals",
    "goals_per_90": "Goals /90",
    "xg": "xG",
    "xg_per_90": "xG /90",
    "shots": "Shots",
    "shots_per_90": "Shots /90",
    "shots_on_target_%": "Shots On Target %",
    "goal_conversion_%": "Goal Conversion %",
    "non-penalty_goals": "Non-Penalty Goals",
    "non-penalty_goals_per_90": "Non-Penalty Goals /90",
    "non_penalty_xg": "Non-Penalty xG",
    "non_penalty_xg_per_90": "Non-Penalty xG /90",
    "touches_in_box_per_90": "Touches In Box /90",
    "head_goals": "Head Goals",
    "head_goals_per_90": "Head Goals /90",
    "penalties_taken": "Penalties Taken",
    "penalty_conversion_%": "Penalty Conversion %",

    # =================
    # Creativity / Chance Creation
    # =================
    "assists": "Assists",
    "assists_per_90": "Assists /90",
    "xa": "xA",
    "xa_per_90": "xA /90",
    "xa_per_100_passes": "xA / 100 Passes",
    "shot_assists_per_90": "Shot Assists /90",
    "key_passes_per_90": "Key Passes /90",
    "key_passes_per_100_passes": "Key Passes / 100 Passes",
    "smart_passes_per_90": "Smart Passes /90",
    "accurate_smart_passes_%": "Accurate Smart Passes %",
    "through_passes_per_90": "Through Passes /90",
    "accurate_through_passes_%": "Accurate Through Passes %",
    "second_assists_per_90": "Second Assists /90",
    "third_assists_per_90": "Third Assists /90",

    # =================
    # General Passing / Distribution
    # =================
    "passes_per_90": "Passes /90",
    "accurate_passes_%": "Accurate Passes %",
    "forward_passes_per_90": "Forward Passes /90",
    "accurate_forward_passes_%": "Accurate Forward Passes %",
    "back_passes_per_90": "Back Passes /90",
    "accurate_back_passes_%": "Accurate Back Passes %",
    "lateral_passes_per_90": "Lateral Passes /90",
    "accurate_lateral_passes_%": "Accurate Lateral Passes %",
    "short_/_medium_passes_per_90": "Short / Medium Passes /90",
    "accurate_short_/_medium_passes_%": "Accurate Short / Medium Passes %",
    "received_passes_per_90": "Received Passes /90",
    "received_long_passes_per_90": "Received Long Passes /90",
    "average_pass_length_m": "Average Pass Length M",

    # =================
    # Progression / Penetration
    # =================
    "progressive_passes_per_90": "Progressive Passes /90",
    "accurate_progressive_passes_%": "Accurate Progressive Passes %",
    "progressive_runs_per_90": "Progressive Runs /90",
    "passes_to_final_third_per_90": "Passes To Final Third /90",
    "accurate_passes_to_final_third_%": "Accurate Passes To Final Third %",
    "passes_to_penalty_area_per_90": "Passes To Penalty Area /90",
    "accurate_passes_to_penalty_area_%": "Accurate Passes To Penalty Area %",
    "deep_completions_per_90": "Deep Completions /90",

    # =================
    # Long Passing
    # =================
    "long_passes_per_90": "Long Passes /90",
    "accurate_long_passes_%": "Accurate Long Passes %",
    "average_long_pass_length_m": "Average Long Pass Length M",

    # =================
    # Crossing / Delivery
    # =================
    "crosses_per_90": "Crosses /90",
    "accurate_crosses_%": "Accurate Crosses %",
    "crosses_from_left_flank_per_90": "Crosses From Left Flank /90",
    "accurate_crosses_from_left_flank_%": "Accurate Crosses From Left Flank %",
    "crosses_from_right_flank_per_90": "Crosses From Right Flank /90",
    "accurate_crosses_from_right_flank_%": "Accurate Crosses From Right Flank %",
    "crosses_to_goalie_box_per_90": "Crosses To Goalie Box /90",
    "deep_completed_crosses_per_90": "Deep Completed Crosses /90",

    # =================
    # Dribbling / 1v1 Ability
    # =================
    "dribbles_per_90": "Dribbles /90",
    "successful_dribbles_%": "Successful Dribbles %",
    "offensive_duels_per_90": "Offensive Duels /90",
    "offensive_duels_won_%": "Offensive Duels Won %",
    "successful_attacking_actions_per_90": "Successful Attacking Actions /90",
    "fouls_suffered_per_90": "Fouls Suffered /90",
    "accelerations_per_90": "Accelerations /90",

    # =================
    # Duels / Physical Contest
    # =================
    "duels_per_90": "Duels /90",
    "duels_won_%": "Duels Won %",

    # =================
    # Defending / Discipline
    # =================
    "successful_defensive_actions_per_90": "Successful Defensive Actions /90",
    "defensive_duels_per_90": "Defensive Duels /90",
    "defensive_duels_won_%": "Defensive Duels Won %",
    "interceptions_per_90": "Interceptions /90",
    "padj_interceptions": "PAdj Interceptions",
    "p_adj_interceptions": "PAdj Interceptions",
    "shots_blocked_per_90": "Shots Blocked /90",
    "sliding_tackles_per_90": "Sliding Tackles /90",
    "padj_sliding_tackles": "PAdj Sliding Tackles",
    "p_adj_sliding_tackles": "PAdj Sliding Tackles",
    "fouls_per_90": "Fouls /90",
    "yellow_cards": "Yellow Cards",
    "yellow_cards_per_90": "Yellow Cards /90",
    "red_cards": "Red Cards",
    "red_cards_per_90": "Red Cards /90",

    # =================
    # Aerial Ability
    # =================
    "aerial_duels_per_90": "Aerial Duels /90",
    "aerial_duels_won_%": "Aerial Duels Won %",

    # =================
    # Set Pieces
    # =================
    "free_kicks_per_90": "Free Kicks /90",
    "direct_free_kicks_per_90": "Direct Free Kicks /90",
    "direct_free_kicks_on_target_%": "Direct Free Kicks On Target %",
    "corners_per_90": "Corners /90",

    # =================
    # Goalkeeper
    # =================
    "conceded_goals": "Conceded Goals",
    "conceded_goals_per_90": "Conceded Goals /90",
    "shots_against": "Shots Against",
    "shots_against_per_90": "Shots Against /90",
    "clean_sheets": "Clean Sheets",
    "save_rate_%": "Save Rate %",
    "xg_against": "xG Against",
    "xg_against_per_90": "xG Against /90",
    "prevented_goals": "Prevented Goals",
    "prevented_goals_per_90": "Prevented Goals /90",
    "back_passes_received_as_gk_per_90": "Back Passes Received As GK /90",
    "exits_per_90": "Exits /90",
    "aerial_duels_per_90.1": "Aerial Duels /90.1",
    "aerial_duels_per_90_1": "Aerial Duels /90.1",
}



# =================
# FEATURE HELPERS
# =================
def get_role_for_position(position: str) -> str:
    """Return the generic role for a given position."""
    return POSITION_TO_ROLE.get(position, "CF")


def get_feature_groups_for_position(position: str, profile: str = None) -> dict:
    """Return grouped features for the player's role."""

    role = get_role_for_position(position)
    if profile:
        role = f"{role}_{profile}"
        print()
    return FEATURE_GROUPS_BY_ROLE[role]


def get_all_features_for_position(position: str, profile: str = None) -> list:
    """Flatten all feature groups into a single ordered list."""

    feature_groups = get_feature_groups_for_position(position, profile=profile)
    return [feature for group in feature_groups.values() for feature in group]


def get_comparison_group_for_position(position: str) -> str:
    return POSITION_TO_COMPARISON_GROUP.get(position, position)


def compute_percentiles(df, features, position=None):
    df_pct = df.copy()

    if position:
        comparison_group = get_comparison_group_for_position(position)
        valid_positions = COMPARISON_GROUPS.get(comparison_group, [position])
        df_pct = df_pct[df_pct["main_position"].isin(valid_positions)].copy()

    for col in features:
        df_pct[col] = pd.to_numeric(df_pct[col], errors="coerce")
        df_pct[col] = df_pct[col].fillna(df_pct[col].median())
        df_pct[col] = rankdata(df_pct[col], method="average") / len(df_pct) * 100

    return df_pct


def get_feature_colors(features: list, position: str, profile: str = None):
    """Return a color for each feature based on its group."""
    
    role = get_role_for_position(position)
    if profile:
        role = f"{role}_{profile}"
        
    feature_groups = FEATURE_GROUPS_BY_ROLE[role]

    colors = []

    for feature in features:
        color = "#999999"

        for group_name, group_features in feature_groups.items():
            if feature in group_features:
                color = GROUP_COLORS.get(group_name, "#999999")
                break

        colors.append(color)

    return colors

def lighten_color(color, amount=0.5):
    """Create a lighter version of a given color for the background layer."""
    try:
        color = mc.cnames[color]
    except Exception:
        pass

    hue, lightness, saturation = colorsys.rgb_to_hls(*mc.to_rgb(color))
    return colorsys.hls_to_rgb(hue, 1 - amount * (1 - lightness), saturation)

def darken_color(color, amount=0.75):
    """Return a darker version of a given color."""
    try:
        color = mc.cnames[color]
    except Exception:
        pass

    hue, lightness, saturation = colorsys.rgb_to_hls(*mc.to_rgb(color))
    return colorsys.hls_to_rgb(hue, lightness * amount, saturation)

def sanitize_filename(value: str) -> str:
    """Make a string safe to use in a filename."""
    return (
        str(value)
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace("-", "_")
    )

# =================
# PIZZA CHART
# =================
def plot_player_profile(
    df: pd.DataFrame,
    player_names: str | list[str],
    minimum_minutes_played: int,
    profile: str = None,
    mode="position",
    save_path = None
):
    """
    Plot one or more player pizza charts.

    mode='position' -> compare the player only with players in the same position
    mode='all'      -> compare the player with all players in the dataframe
    """
    # Keep only players above the minimum minutes threshold
    df = df[df["minutes_played"] >= minimum_minutes_played].copy()

    # Accept either one player name or a list of player names
    if isinstance(player_names, str):
        player_names = [player_names]

    n_players = len(player_names)

    # Figure size grows depending on how many players will be shown
    width_per_plot = 12.0
    fig_width = max(12.5, width_per_plot * n_players)
    fig_height = 8.8

    # Create polar subplots because pizza charts are radial plots
    fig, axes = plt.subplots(
        1,
        n_players,
        figsize=(fig_width, fig_height),
        subplot_kw=dict(polar=True),
        dpi=150,
    )

    if n_players == 1:
        axes = [axes]

    # Adjust chart spacing inside the figure
    plt.subplots_adjust(
        left=0.05,
        right=0.95,
        top=0.82,
        bottom=0.30,
        wspace=0.15,
    )

    plotted_players = []

    last_position = None

    for ax, player_name in zip(axes, player_names):
        # Get the selected player's row
        player_row = df[df["player"] == player_name]

        if player_row.empty:
            print(f"{player_name} not found")
            continue

        # Player basic info
        position = player_row["main_position"].values[0]
        team = player_row["team"].values[0]
        last_position = position
        league = player_row["league_name"].values[0]
        season = player_row["season"].values[0] if "season" in player_row.columns else "unknown_season"

        plotted_players.append(
            {
                "player": player_name,
                "team": team,
                "season": season,
                "position": position,
            }
        )
        # if profile:
        #     position = f"{position}_{profile}"

        # Features used in the chart depend on the player's position
        features = get_all_features_for_position(position=position, profile=profile)
        
        # The number of players used for comparison (either same position or whole dataset)
        total_players_comparison = df.shape[0] - 1

        # Compute percentile ranks
        if mode == "position":
            df_pct = compute_percentiles(df, features, position=position)
            
            comparison_group = get_comparison_group_for_position(position)
            print(f"Comparison group for position {position}: {comparison_group}")
            valid_positions = COMPARISON_GROUPS.get(comparison_group, [position])
            print(f"Valid positions for comparison: {valid_positions}")
            total_players_comparison = df[df["main_position"].isin(valid_positions)].shape[0] - 1
        else:
            df_pct = compute_percentiles(df, features)

        # Get the selected player's percentile values
        values = df_pct.loc[
            df_pct["player"] == player_name,
            features
        ].values.flatten()

        values = np.nan_to_num(values, nan=0).round(1)

        # Labels shown around the chart
        features_wrapped = [
            FEATURE_LABELS.get(feature, feature).replace(" ", "\n")
            for feature in features
        ]

        # Slice colors depend on feature group
        slice_colors = get_feature_colors(position=position, profile=profile, features=features)
        foreground_slice_colors = [darken_color(color, 0.88) for color in slice_colors]
        background_slice_colors = [lighten_color(color, 0.74) for color in slice_colors]

        # Pizza chart styling
        baker = PyPizza(
            params=features_wrapped,
            background_color=BRAND_COLORS["background_main"],
            straight_line_color=BRAND_COLORS["border"],
            straight_line_lw=1,
            last_circle_lw=1,
            last_circle_color=BRAND_COLORS["border"],
            other_circle_lw=0,
            inner_circle_size=32
        )

        number_of_features = len(features)

        # Background layer: full 100th percentile, in light colors
        baker.make_pizza(
            [100] * number_of_features,
            ax=ax,
            slice_colors=background_slice_colors,
            kwargs_slices=dict(edgecolor="white", linewidth=1),
            kwargs_values=dict(alpha=0),  # hide values on background layer
            kwargs_params=dict(
                fontsize=0,             # label size around chart
                color=BRAND_COLORS["text_main"],
                weight="bold",
                va="center",
                path_effects=[patheffects.withStroke(linewidth=2, foreground=BRAND_COLORS["background_main"])]
            ),
            param_location=125,
        )

        # Foreground layer: player's real percentile values
        baker.make_pizza(
            values,
            ax=ax,
            slice_colors=foreground_slice_colors,
            kwargs_slices=dict(edgecolor="white", linewidth=1),
            kwargs_values=dict(
                fontsize=7,                            # number size inside slices
                color=BRAND_COLORS["text_main"],  # number color
                alpha=0.95,
                weight="bold",
                bbox=dict(
                    boxstyle="round,pad=0.36,rounding_size=1.00",
                    facecolor=BRAND_COLORS["background_main"],
                    alpha=0.90,
                    edgecolor="none",
                )
            ),
            kwargs_params=dict(
                fontsize=7,             # label size around chart
                color=BRAND_COLORS["text_main"],
                weight="bold",
                va="center",
                path_effects=[patheffects.withStroke(linewidth=2, foreground=BRAND_COLORS["background_main"])]
            ),
            param_location=125,
        )
        
        # Force all value labels to stay around the 75% ring
        for text in baker.get_value_texts():
            value = float(text.get_text())
            
            if value.is_integer():
                text.set_text(str(int(value)))
            else:
                text.set_text(f"{value:.1f}")
                
            if value > 91:
                text.set_y(88)
            
            text.set_ha("center")
            text.set_va("center")

        # Title above each player's chart
        # ax.set_title(
        #     f"{player_name} | {team}\n{position}\n",
        #     fontproperties=font_bold,
        #     color=BRAND_COLORS["text_main"],
        #     y=1.14,
        # )

    # Build legend using the feature groups of the plotted position
    if last_position is not None:
        feature_groups = get_feature_groups_for_position(position=last_position, profile=profile)

        legend_elements = [
            Patch(facecolor=GROUP_COLORS[group], label=group)
            for group in feature_groups.keys()
        ]

        if n_players == 1:
            legend_ncol = 2
            legend_y = 0.10
        else:
            legend_ncol = len(feature_groups)
            legend_y = 0.08

        fig.legend(
            handles=legend_elements,
            loc="lower center",
            bbox_to_anchor=(0.5, legend_y),
            ncol=legend_ncol,
            frameon=False,
            fontsize=13,
            labelcolor=BRAND_COLORS["text_main"]
        )

    # Footer text below the chart
    footer_mode = "vs Position" if mode == "position" else "vs All Players"

    if n_players == 1:
        footer_text = (
            f"\nPercentile Rank ({footer_mode})\n"
            f"Compared to {total_players_comparison} {comparison_group} players\n"
            f"{minimum_minutes_played}+ minutes | {league} - {season}"
            # f"Illustrative example using Wyscout data"
        )
        footer_y = 0.015
    else:
        footer_text = (
            f"\nPercentile Rank ({footer_mode})"
        )
        footer_y = 0.01

    fig.text(
        0.5,
        footer_y,
        footer_text,
        ha="center",
        fontsize=13,
        color=BRAND_COLORS["text_muted"]
    )
    fig.patch.set_facecolor(BRAND_COLORS["background_main"])

    if save_path is None and plotted_players:
        if len(plotted_players) == 1:
            player_info = plotted_players[0]
            filename = (
                f"{sanitize_filename(player_info['player'])}_"
                f"{sanitize_filename(player_info['team'])}_"
                f"{sanitize_filename(player_info['season'])}_pizza_chart.png"
            )
        else:
            joined_names = "_vs_".join(
                sanitize_filename(player_info["player"])
                for player_info in plotted_players
            )
            filename = f"{joined_names}_pizza_chart.png"

        save_path = Path(filename)

    # if save_path:
    #     plt.savefig(
    #         save_path,
    #         dpi=300,
    #         bbox_inches="tight",
    #         facecolor=fig.get_facecolor()
    #     )

    # plt.show()
    
    return fig, plotted_players