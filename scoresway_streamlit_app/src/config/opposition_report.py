# =========================
# OPPOSITION REPORT CONFIG
# =========================

OPPOSITION_HIGH_SCORE_THRESHOLD = 70
OPPOSITION_LOW_SCORE_THRESHOLD = 40


OPPOSITION_STYLE_RULES = {
    "possession_control_score": {
        "area": "attack",
        "label": "Possession Control",
        "high": "Ball-dominant profile. They are likely to spend longer periods circulating possession.",
        "medium": "Balanced possession profile. They can keep the ball, but possession is not clearly dominant.",
        "low": "Lower possession profile. They may be more comfortable playing without long control phases.",
        "prep_high": "Prepare compact defensive spacing and clear pressing triggers against longer possession phases.",
        "vulnerability_low": "They may be less comfortable if forced to build patiently under pressure.",
    },

    "territory_penetration_score": {
        "area": "attack",
        "label": "Territory & Penetration",
        "high": "Strong territory profile. They reach advanced areas often and can sustain pressure.",
        "medium": "Moderate territory profile. They can access advanced zones, but not consistently.",
        "low": "Limited territory profile. They may struggle to sustain attacks high up the pitch.",
        "prep_high": "Protect central access and reduce repeated final-third entries.",
        "vulnerability_low": "They may leave room to defend higher if their progression is limited.",
    },

    "attacking_volume_score": {
        "area": "attack",
        "label": "Attacking Volume",
        "high": "High attacking volume. They generate frequent shots and chance-creation actions.",
        "medium": "Moderate attacking volume. Their chance creation exists, but is not overwhelming.",
        "low": "Low attacking volume. They may rely more on efficiency, transitions or set pieces.",
        "prep_high": "Limit shot volume early by controlling second balls and defending the edge of the box.",
        "vulnerability_low": "They may struggle to create enough volume if denied transitions and set pieces.",
    },

    "directness_score": {
        "area": "attack",
        "label": "Directness",
        "high": "Direct profile. They can gain territory quickly through longer passes and second balls.",
        "medium": "Mixed directness profile. They can go long, but are not fully direct.",
        "low": "Less direct profile. They are less reliant on long passes or launch volume.",
        "prep_high": "Prepare depth protection, aerial duels and second-ball reactions.",
        "vulnerability_low": "They may be easier to slow down if short progression lanes are blocked.",
    },

    "width_crossing_score": {
        "area": "attack",
        "label": "Width & Crossing",
        "high": "Wide and crossing-oriented profile. They use wide areas and delivery into the box regularly.",
        "medium": "Moderate wide-play profile. They use width, but it is not necessarily the main route.",
        "low": "Lower crossing profile. They may attack more centrally or through other routes.",
        "prep_high": "Prepare wide defending, box occupation and far-post coverage.",
        "vulnerability_low": "They may offer less threat if central progression is blocked and they are forced wide.",
    },

    "set_piece_threat_score": {
        "area": "attack",
        "label": "Set-Piece Threat",
        "high": "Set-piece threat. Dead-ball preparation should be a priority.",
        "medium": "Moderate set-piece threat. They can be dangerous, but it may not be a core weapon.",
        "low": "Lower set-piece threat. Set pieces still matter, but are not a standout strength.",
        "prep_high": "Add a specific preparation block for defensive set pieces.",
        "vulnerability_low": "They may have limited alternative threat if open-play creation is also low.",
    },

    "pressing_ball_winning_score": {
        "area": "defence",
        "label": "Pressing & Ball Winning",
        "high": "Aggressive ball-winning profile. They are likely to challenge build-up phases actively.",
        "medium": "Moderate pressing profile. They can press, but it may not define their whole game model.",
        "low": "Lower pressing profile. They may defend in more controlled or deeper phases.",
        "prep_high": "Build-up structure must include clear support angles and escape routes.",
        "vulnerability_low": "They may allow more controlled progression if the first line is bypassed.",
    },

    "defensive_resistance_score": {
        "area": "defence",
        "label": "Defensive Resistance",
        "high": "Strong defensive resistance. They are harder to break down and limit opposition output well.",
        "medium": "Moderate defensive resistance. They are not clearly weak, but can still be attacked.",
        "low": "Defensive vulnerability indicator. There may be space to create shots or sustain pressure.",
        "prep_high": "Attacks may require patience, switches of play and strong occupation between lines.",
        "vulnerability_low": "There may be potential to create volume if pressure is sustained.",
    },

    "physicality_duels_score": {
        "area": "defence",
        "label": "Physicality / Duels",
        "high": "Duel-heavy profile. Physical contests, aerial balls and second balls are important.",
        "medium": "Moderate duel profile. Physical contests matter, but do not fully define the game.",
        "low": "Lower duel-volume profile. The match may be less based on repeated physical contests.",
        "prep_high": "Prepare for aerial contests, contact situations and loose-ball reactions.",
        "vulnerability_low": "They may be less comfortable if the game becomes more physical and duel-heavy.",
    },
}