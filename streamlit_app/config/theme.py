import streamlit as st


BRAND_COLORS = {
    # Backgrounds
    "background_main": "#0F172A",
    "background_panel": "#1E293B",
    "background_card": "#111827",
    "background_card_dark": "#0B1220",
    "background_card_hover": "#111C30",
    "background_card_light": "#CBD5E1",

    # Text
    "text_main": "#E2E8F0",
    "text_body": "#CBD5E1",
    "text_muted": "#94A3B8",
    "text_white": "#FFFFFF",

    # Borders
    "border": "#334155",
    "border_light": "#475569",

    # Accent
    "accent": "#CBD5E1",
    "accent_text": "#0F172A",
    "accent_dark": "#0F172A",

    # Feedback
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "success": "#22C55E",
}


def apply_theme() -> None:
    st.markdown(
        f"""
        <style>
            /* =========================
               Global App
            ========================= */

            .stApp {{
                background-color: {BRAND_COLORS["background_main"]};
                color: {BRAND_COLORS["text_main"]};
            }}

            h1, h2, h3, h4, h5, h6 {{
                color: {BRAND_COLORS["text_main"]};
            }}

            p, label, span, div {{
                color: {BRAND_COLORS["text_body"]};
            }}

            hr {{
                border-color: {BRAND_COLORS["border"]};
            }}

            section[data-testid="stSidebar"] {{
                background-color: {BRAND_COLORS["background_panel"]};
                border-right: 1px solid {BRAND_COLORS["border"]};
            }}


            /* =========================
               Streamlit Widget Overrides
            ========================= */

            /* Segmented control selected option */
            div[data-testid="stSegmentedControl"] button[aria-pressed="true"] {{
                background-color: {BRAND_COLORS["accent"]} !important;
                color: {BRAND_COLORS["accent_text"]} !important;
                border-color: {BRAND_COLORS["accent"]} !important;
            }}

            div[data-testid="stSegmentedControl"] button[aria-pressed="true"] p {{
                color: {BRAND_COLORS["accent_text"]} !important;
            }}

            /* Radio selected dot */
            div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {{
                border-color: {BRAND_COLORS["accent"]} !important;
            }}

            div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child > div {{
                background-color: {BRAND_COLORS["accent"]} !important;
            }}

            /* Buttons */
            div[data-testid="stButton"] > button {{
                border-radius: 12px;
                border: 1px solid {BRAND_COLORS["border_light"]};
                background-color: rgba(203, 213, 225, 0.08);
                color: {BRAND_COLORS["accent"]};
                font-weight: 700;
            }}

            div[data-testid="stButton"] > button:hover {{
                border-color: {BRAND_COLORS["accent"]};
                background-color: {BRAND_COLORS["accent"]};
                color: {BRAND_COLORS["accent_text"]};
            }}

            /* Slider */
            div[data-testid="stSlider"] div[role="slider"] {{
                background-color: {BRAND_COLORS["text_white"]} !important;
                border-color: {BRAND_COLORS["text_white"]} !important;
            }}


            /* =========================
               Page Header
            ========================= */

            .team-header {{
                background: linear-gradient(
                    135deg,
                    {BRAND_COLORS["background_card"]} 0%,
                    {BRAND_COLORS["background_panel"]} 55%,
                    {BRAND_COLORS["background_main"]} 100%
                );
                border: 1px solid {BRAND_COLORS["border"]};
                border-radius: 22px;
                padding: 28px 32px;
                margin-bottom: 28px;
                box-shadow: 0 18px 45px rgba(0, 0, 0, 0.22);
            }}

            .team-header-kicker {{
                font-size: 0.78rem;
                text-transform: uppercase;
                letter-spacing: 0.14em;
                color: {BRAND_COLORS["text_muted"]};
                font-weight: 700;
                margin-bottom: 10px;
            }}

            .team-header-title {{
                font-size: 2.7rem;
                line-height: 1.05;
                font-weight: 800;
                color: {BRAND_COLORS["text_main"]};
                margin-bottom: 12px;
            }}

            .team-header-meta {{
                display: flex;
                gap: 10px;
                align-items: center;
                flex-wrap: wrap;
            }}

            .team-header-pill {{
                background-color: rgba(203, 213, 225, 0.10);
                color: {BRAND_COLORS["accent"]};
                border: 1px solid rgba(203, 213, 225, 0.22);
                border-radius: 999px;
                padding: 6px 12px;
                font-size: 0.85rem;
                font-weight: 600;
            }}


            /* =========================
               KPI Cards
            ========================= */

            .kpi-card {{
                background: {BRAND_COLORS["accent"]};
                border: 1px solid {BRAND_COLORS["text_main"]};
                border-radius: 16px;
                padding: 14px 16px;
                min-height: 96px;
                box-shadow: 0 10px 24px rgba(0, 0, 0, 0.16);

                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
            }}

            .kpi-label {{
                color: {BRAND_COLORS["accent_text"]};
                opacity: 0.75;
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 8px;
            }}

            .kpi-value {{
                color: {BRAND_COLORS["accent_text"]};
                font-size: 1.95rem;
                line-height: 1;
                font-weight: 800;
            }}

            .kpi-subtitle {{
                color: {BRAND_COLORS["accent_text"]};
                opacity: 0.65;
                font-size: 0.72rem;
                margin-top: 6px;
            }}


            /* =========================
               Generic Entity Grid Cards
               Used for leagues, teams, etc.
            ========================= */

            .entity-grid {{
                display: grid;
                grid-template-columns: repeat(6, minmax(0, 1fr));
                gap: 14px;
                width: 100%;
                margin-top: 12px;
            }}

            .entity-card,
            .entity-action-card {{
                min-height: 96px;
                padding: 14px;

                display: flex;
                flex-direction: column;
                justify-content: space-between;
                gap: 10px;

                background: {BRAND_COLORS["background_panel"]};
                border: 1px solid {BRAND_COLORS["border"]};
                border-radius: 16px;

                color: {BRAND_COLORS["text_main"]};
                text-decoration: none !important;

                box-shadow: 0 10px 24px rgba(0, 0, 0, 0.14);

                transition:
                    background-color 0.16s ease,
                    border-color 0.16s ease,
                    transform 0.16s ease,
                    box-shadow 0.16s ease;
            }}

            .entity-action-card {{
                min-height: 112px;
            }}

            .entity-card:hover,
            .entity-action-card:hover {{
                background-color: rgba(203, 213, 225, 0.08);
                border-color: {BRAND_COLORS["accent"]};
                transform: translateY(-2px);
                box-shadow: 0 14px 32px rgba(0, 0, 0, 0.22);
            }}

            .entity-card-top {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}

            .entity-card-badge {{
                width: 34px;
                height: 34px;
                min-width: 34px;
                border-radius: 999px;

                display: flex;
                align-items: center;
                justify-content: center;

                background-color: rgba(203, 213, 225, 0.12);
                border: 1px solid rgba(203, 213, 225, 0.24);

                color: {BRAND_COLORS["text_main"]};
                font-size: 0.72rem;
                font-weight: 800;
            }}

            .entity-card:hover .entity-card-badge,
            .entity-action-card:hover .entity-card-badge {{
                background-color: {BRAND_COLORS["accent"]};
                color: {BRAND_COLORS["accent_text"]};
            }}

            .entity-card-title {{
                color: {BRAND_COLORS["text_main"]};
                font-size: 0.88rem;
                font-weight: 800;
                line-height: 1.18;

                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;

                overflow: hidden;
                text-overflow: ellipsis;
            }}

            .entity-card:hover .entity-card-title,
            .entity-action-card:hover .entity-card-title {{
                color: {BRAND_COLORS["accent"]};
            }}

            .entity-card-subtitle {{
                color: {BRAND_COLORS["text_muted"]};
                font-size: 0.75rem;
                font-weight: 600;
            }}

            .entity-card-meta {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
                width: 100%;
                margin-top: 8px;
                color: {BRAND_COLORS["text_muted"]};
                font-size: 0.78rem;
                line-height: 1.2;
            }}

            .entity-card-country {{
                min-width: 0;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                color: {BRAND_COLORS["text_muted"]};
                font-weight: 700;
            }}

            .entity-card-seasons {{
                flex-shrink: 0;
                text-align: right;
                color: {BRAND_COLORS["text_body"]};
                font-weight: 500;
            }}


            /* =========================
               Team List Rows
               Used for compact vertical team lists
            ========================= */

            .team-list-container {{
                width: 100%;
                background: {BRAND_COLORS["background_panel"]};
                border: 1px solid {BRAND_COLORS["border"]};
                border-radius: 18px;
                overflow: hidden;
                box-shadow: 0 14px 34px rgba(0, 0, 0, 0.18);
            }}

            .team-list-row {{
                display: flex;
                align-items: center;
                gap: 14px;

                width: 100%;
                min-height: 58px;
                padding: 12px 18px;

                text-decoration: none !important;
                border-left: 4px solid transparent;
                border-bottom: 1px solid rgba(148, 163, 184, 0.14);

                transition:
                    background-color 0.16s ease,
                    border-left-color 0.16s ease,
                    transform 0.16s ease;
            }}

            .team-list-row:last-child {{
                border-bottom: none;
            }}

            .team-list-row:hover {{
                background-color: rgba(203, 213, 225, 0.08);
                border-left-color: {BRAND_COLORS["accent"]};
                transform: translateX(2px);
            }}

            .team-badge {{
                width: 36px;
                height: 36px;
                min-width: 36px;
                border-radius: 999px;

                display: flex;
                align-items: center;
                justify-content: center;

                background-color: rgba(203, 213, 225, 0.12);
                border: 1px solid rgba(203, 213, 225, 0.24);

                color: {BRAND_COLORS["text_main"]};
                font-size: 0.72rem;
                font-weight: 800;
            }}

            .team-name {{
                color: {BRAND_COLORS["text_main"]};
                font-size: 1rem;
                font-weight: 700;
                line-height: 1.2;

                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}

            .team-list-row:hover .team-name {{
                color: {BRAND_COLORS["accent"]};
            }}

            .team-list-row:hover .team-badge {{
                background-color: {BRAND_COLORS["accent"]};
                color: {BRAND_COLORS["accent_text"]};
            }}


            /* =========================
               Player List Table
            ========================= */

            .player-list-wrapper {{
                width: 100%;
                border: 1px solid {BRAND_COLORS["border"]};
                border-radius: 10px;
                overflow: hidden;
                background: {BRAND_COLORS["background_card_dark"]};
            }}

            .player-list-header {{
                display: grid;
                background: {BRAND_COLORS["background_panel"]};
                border-bottom: 1px solid {BRAND_COLORS["border"]};
            }}

            .player-list-row {{
                display: grid;
                border-bottom: 1px solid rgba(51, 65, 85, 0.65);
                background: {BRAND_COLORS["background_main"]};
                transition: background 0.15s ease;
                text-decoration: none !important;
            }}

            .player-list-row:last-child {{
                border-bottom: none;
            }}

            .player-list-row:hover {{
                background: {BRAND_COLORS["background_card_hover"]};
            }}

            .player-list-row-link {{
                cursor: pointer;
                color: inherit;
                text-decoration: none !important;
            }}

            .player-list-row-link:hover {{
                background: {BRAND_COLORS["background_card_hover"]};
                cursor: pointer;
                text-decoration: none !important;
            }}

            .player-list-row-link:hover .player-list-cell {{
                color: {BRAND_COLORS["text_white"]};
                text-decoration: none !important;
            }}

            .player-list-cell {{
                min-width: 0;
                padding: 10px 12px;
                color: {BRAND_COLORS["text_main"]};
                font-size: 0.82rem;
                line-height: 1.25;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }}

            .player-list-header-cell {{
                display: flex;
                align-items: center;
                gap: 6px;
                color: {BRAND_COLORS["text_body"]};
                font-size: 0.78rem;
                font-weight: 600;
                text-decoration: none;
                background: {BRAND_COLORS["background_panel"]};
            }}

            .player-list-header-cell:hover {{
                color: {BRAND_COLORS["text_white"]};
                background: #263449;
            }}

            .sort-icon {{
                color: {BRAND_COLORS["text_muted"]};
                font-size: 0.75rem;
            }}

            .align-left {{
                text-align: left;
                justify-content: flex-start;
            }}

            .align-center {{
                text-align: center;
                justify-content: center;
            }}

            .align-right {{
                text-align: right;
                justify-content: flex-end;
            }}
            
            /* =========================
            Player Profile Header
            ========================= */

            .player-profile-header {{
                background: linear-gradient(
                    135deg,
                    {BRAND_COLORS["background_card"]} 0%,
                    {BRAND_COLORS["background_panel"]} 65%,
                    {BRAND_COLORS["background_main"]} 100%
                );
                border: 1px solid {BRAND_COLORS["border"]};
                border-radius: 18px;
                padding: 24px 28px;
                margin-bottom: 20px;
                box-shadow: 0 14px 34px rgba(0, 0, 0, 0.18);
            }}

            .player-profile-header-content {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 24px;
            }}

            .player-profile-kicker {{
                color: {BRAND_COLORS["text_muted"]};
                font-size: 0.72rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.14em;
                margin-bottom: 8px;
            }}

            .player-profile-title {{
                color: {BRAND_COLORS["text_main"]};
                font-size: 2.25rem;
                line-height: 1.05;
                font-weight: 900;
                margin-bottom: 12px;
            }}

            .player-profile-meta {{
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }}

            .player-profile-meta span {{
                background-color: rgba(203, 213, 225, 0.09);
                color: {BRAND_COLORS["text_body"]};
                border: 1px solid rgba(203, 213, 225, 0.20);
                border-radius: 999px;
                padding: 5px 10px;
                font-size: 0.78rem;
                font-weight: 650;
            }}

            .player-profile-position {{
                width: 64px;
                height: 64px;
                min-width: 64px;

                display: flex;
                align-items: center;
                justify-content: center;

                background: {BRAND_COLORS["accent"]};
                color: {BRAND_COLORS["accent_text"]};
                border-radius: 16px;

                font-size: 1.2rem;
                font-weight: 900;
                box-shadow: 0 10px 24px rgba(0, 0, 0, 0.20);
            }}
            
            /* Make segmented control smaller inside player header */
            .player-profile-season-row div[data-testid="stSegmentedControl"] {{
                margin-top: 0;
            }}

            .player-profile-season-row div[data-testid="stSegmentedControl"] button {{
                padding: 5px 12px;
                min-height: 34px;
                font-size: 0.78rem;
                border-radius: 8px;
            }}
            
            /* =========================
            Player Bio Strip
            ========================= */

            .player-bio-grid {{
                display: grid;
                grid-template-columns: repeat(8, minmax(0, 1fr));
                gap: 10px;
                margin-bottom: 22px;
            }}

            .player-bio-card {{
                background: {BRAND_COLORS["background_panel"]};
                border: 1px solid {BRAND_COLORS["border"]};
                border-radius: 14px;
                padding: 11px 12px;
                min-height: 72px;

                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;

                text-align: center;

                box-shadow: 0 8px 18px rgba(0, 0, 0, 0.12);
            }}

            .player-bio-label {{
                color: {BRAND_COLORS["text_muted"]};
                font-size: 0.67rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.07em;
                margin-bottom: 5px;
                text-align: center;
            }}

            .player-bio-value {{
                color: {BRAND_COLORS["text_main"]};
                font-size: 0.95rem;
                font-weight: 800;
                line-height: 1.15;

                text-align: center;

                overflow: hidden;
                text-overflow: ellipsis;
            }}
            
            .player-tab-panel {{
    background: rgba(30, 41, 59, 0.62);
    border: 1px solid {BRAND_COLORS["border"]};
    border-radius: 16px;
    padding: 16px;
    margin-top: 8px;
}}

.player-tab-title {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 1.05rem;
    font-weight: 850;
    margin-bottom: 4px;
}}

.player-tab-description {{
    color: {BRAND_COLORS["text_muted"]};
    font-size: 0.78rem;
    margin-bottom: 14px;
}}

.profile-metric-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    overflow: hidden;
}}

.profile-metric-card {{
    background: {BRAND_COLORS["background_card"]};
    border-right: 1px solid rgba(51, 65, 85, 0.85);
    border-bottom: 1px solid rgba(51, 65, 85, 0.85);
    padding: 12px 10px;
    min-height: 74px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.profile-metric-card:nth-child(4n) {{
    border-right: none;
}}

.profile-metric-value {{
    color: {BRAND_COLORS["text_body"]};
    font-size: 1.28rem;
    line-height: 1;
    font-weight: 850;
    margin-bottom: 6px;
}}

.profile-metric-label {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.70rem;
    font-weight: 700;
    line-height: 1.15;
    text-align: center;
}}

.profile-metric-subtitle {{
    color: {BRAND_COLORS["text_muted"]};
    font-size: 0.68rem;
    margin-top: 4px;
}}

/* =========================
   Player Attack Panel
========================= */

.attack-panel {{
    background: rgba(30, 41, 59, 0.62);
    border: 1px solid {BRAND_COLORS["border"]};
    border-radius: 16px;
    padding: 16px;
    margin-top: 8px;
}}

.attack-panel-title {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 1.05rem;
    font-weight: 850;
    margin-bottom: 4px;
}}

.attack-panel-description {{
    color: {BRAND_COLORS["text_muted"]};
    font-size: 0.78rem;
    margin-bottom: 14px;
}}

.attack-layout {{
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 14px;
    margin-bottom: 14px;
}}

.attack-box {{
    background: {BRAND_COLORS["background_card"]};
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    padding: 14px;
}}

.attack-box-title {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.82rem;
    font-weight: 800;
    margin-bottom: 12px;
}}

.attack-bar-row {{
    display: grid;
    grid-template-columns: 150px 1fr 52px;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}}

.attack-bar-row:last-child {{
    margin-bottom: 0;
}}

.attack-bar-label {{
    color: {BRAND_COLORS["text_body"]};
    font-size: 0.76rem;
    font-weight: 700;
    line-height: 1.15;
}}

.attack-bar-track {{
    width: 100%;
    height: 12px;
    background: rgba(203, 213, 225, 0.13);
    border-radius: 999px;
    overflow: hidden;
}}

.attack-bar-fill {{
    height: 100%;
    background: {BRAND_COLORS["accent"]};
    border-radius: 999px;
}}

.attack-bar-value {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 1rem;
    font-weight: 850;
    text-align: right;
}}

.attack-efficiency-grid {{
    display: grid;
    grid-template-columns: repeat(1, minmax(0, 1fr));
    gap: 10px;
}}

.attack-efficiency-card {{
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 12px;
    padding: 13px 12px;
    text-align: center;
}}

.attack-efficiency-value {{
    color: {BRAND_COLORS["text_body"]};
    font-size: 1.35rem;
    line-height: 1;
    font-weight: 900;
    margin-bottom: 6px;
}}

.attack-efficiency-label {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.70rem;
    font-weight: 750;
}}

.attack-detail-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    overflow: hidden;
}}

.attack-detail-card {{
    background: {BRAND_COLORS["background_card"]};
    border-right: 1px solid rgba(51, 65, 85, 0.85);
    border-bottom: 1px solid rgba(51, 65, 85, 0.85);
    padding: 13px 10px;
    min-height: 78px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.attack-detail-card:nth-child(4n) {{
    border-right: none;
}}

.attack-detail-value {{
    color: {BRAND_COLORS["text_body"]};
    font-size: 1.35rem;
    line-height: 1;
    font-weight: 900;
    margin-bottom: 6px;
}}

.attack-detail-label {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.70rem;
    font-weight: 750;
    text-align: center;
    line-height: 1.15;
}}

@media (max-width: 1000px) {{
    .attack-layout {{
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }}

    .attack-detail-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}

    .attack-detail-card:nth-child(4n) {{
        border-right: 1px solid rgba(51, 65, 85, 0.85);
    }}

    .attack-detail-card:nth-child(2n) {{
        border-right: none;
    }}
}}

@media (max-width: 700px) {{
    .attack-bar-row {{
        grid-template-columns: 1fr;
        gap: 6px;
    }}

    .attack-bar-value {{
        text-align: left;
    }}

    .attack-detail-grid {{
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }}

    .attack-detail-card {{
        border-right: none;
    }}
}}

/* =========================
   Player Distribution Panel
========================= */

.distribution-panel {{
    background: rgba(30, 41, 59, 0.62);
    border: 1px solid {BRAND_COLORS["border"]};
    border-radius: 16px;
    padding: 16px;
    margin-top: 8px;
}}

.distribution-panel-title {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 1.05rem;
    font-weight: 850;
    margin-bottom: 4px;
}}

.distribution-panel-description {{
    color: {BRAND_COLORS["text_muted"]};
    font-size: 0.78rem;
    margin-bottom: 14px;
}}

.distribution-main-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
    margin-bottom: 14px;
}}

.distribution-box {{
    background: {BRAND_COLORS["background_card"]};
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    padding: 14px;
}}

.distribution-box-title {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.82rem;
    font-weight: 850;
    margin-bottom: 12px;
}}

.distribution-feature-row {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 12px;
    padding: 9px 0;
    border-bottom: 1px solid rgba(148, 163, 184, 0.12);
}}

.distribution-feature-row:last-child {{
    border-bottom: none;
}}

.distribution-feature-label {{
    color: {BRAND_COLORS["text_body"]};
    font-size: 0.75rem;
    font-weight: 700;
    line-height: 1.15;
}}

.distribution-feature-value {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 1.05rem;
    font-weight: 900;
    white-space: nowrap;
}}

.distribution-rate-panel {{
    background: {BRAND_COLORS["background_card"]};
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 14px;
}}

.distribution-rate-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
}}

.distribution-rate-row {{
    width: 100%;
}}

.distribution-rate-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: {BRAND_COLORS["text_body"]};
    font-size: 0.74rem;
    font-weight: 750;
    margin-bottom: 6px;
}}

.distribution-rate-header strong {{
    color: {BRAND_COLORS["text_main"]};
}}

.distribution-rate-track {{
    width: 100%;
    height: 8px;
    background: rgba(203, 213, 225, 0.12);
    border-radius: 999px;
    overflow: hidden;
}}

.distribution-rate-fill {{
    height: 100%;
    background: {BRAND_COLORS["accent"]};
    border-radius: 999px;
}}

.distribution-detail-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    overflow: hidden;
}}

.distribution-detail-card {{
    background: {BRAND_COLORS["background_card"]};
    border-right: 1px solid rgba(51, 65, 85, 0.85);
    border-bottom: 1px solid rgba(51, 65, 85, 0.85);
    padding: 13px 10px;
    min-height: 78px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.distribution-detail-card:nth-child(4n) {{
    border-right: none;
}}

.distribution-detail-value {{
    color: {BRAND_COLORS["text_body"]};
    font-size: 1.25rem;
    line-height: 1;
    font-weight: 900;
    margin-bottom: 6px;
}}

.distribution-detail-label {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.70rem;
    font-weight: 750;
    text-align: center;
    line-height: 1.15;
}}

@media (max-width: 1100px) {{
    .distribution-main-grid {{
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }}

    .distribution-rate-grid,
    .distribution-detail-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}

    .distribution-detail-card:nth-child(4n) {{
        border-right: 1px solid rgba(51, 65, 85, 0.85);
    }}

    .distribution-detail-card:nth-child(2n) {{
        border-right: none;
    }}
}}

@media (max-width: 700px) {{
    .distribution-rate-grid,
    .distribution-detail-grid {{
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }}

    .distribution-detail-card {{
        border-right: none;
    }}
}}

/* =========================
   Player Defence Panel
========================= */

.defence-panel {{
    background: rgba(30, 41, 59, 0.62);
    border: 1px solid {BRAND_COLORS["border"]};
    border-radius: 16px;
    padding: 16px;
    margin-top: 8px;
}}

.defence-panel-title {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 1.05rem;
    font-weight: 850;
    margin-bottom: 4px;
}}

.defence-panel-description {{
    color: {BRAND_COLORS["text_muted"]};
    font-size: 0.78rem;
    margin-bottom: 14px;
}}

.defence-main-grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
    margin-bottom: 14px;
}}

.defence-box {{
    background: {BRAND_COLORS["background_card"]};
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    padding: 14px;
}}

.defence-box-title {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.82rem;
    font-weight: 850;
    margin-bottom: 12px;
}}

.defence-feature-row {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 12px;
    padding: 9px 0;
    border-bottom: 1px solid rgba(148, 163, 184, 0.12);
}}

.defence-feature-row:last-child {{
    border-bottom: none;
}}

.defence-feature-label {{
    color: {BRAND_COLORS["text_body"]};
    font-size: 0.75rem;
    font-weight: 700;
    line-height: 1.15;
}}

.defence-feature-value {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 1.05rem;
    font-weight: 900;
    white-space: nowrap;
}}

.defence-rate-panel {{
    background: {BRAND_COLORS["background_card"]};
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 14px;
}}

.defence-rate-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
}}

.defence-rate-row {{
    width: 100%;
}}

.defence-rate-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: {BRAND_COLORS["text_body"]};
    font-size: 0.74rem;
    font-weight: 750;
    margin-bottom: 6px;
}}

.defence-rate-header strong {{
    color: {BRAND_COLORS["text_main"]};
}}

.defence-rate-track {{
    width: 100%;
    height: 8px;
    background: rgba(203, 213, 225, 0.12);
    border-radius: 999px;
    overflow: hidden;
}}

.defence-rate-fill {{
    height: 100%;
    background: {BRAND_COLORS["accent"]};
    border-radius: 999px;
}}

.defence-detail-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    overflow: hidden;
}}

.defence-detail-card {{
    background: {BRAND_COLORS["background_card"]};
    border-right: 1px solid rgba(51, 65, 85, 0.85);
    border-bottom: 1px solid rgba(51, 65, 85, 0.85);
    padding: 13px 10px;
    min-height: 78px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.defence-detail-card:nth-child(4n) {{
    border-right: none;
}}

.defence-detail-value {{
    color: {BRAND_COLORS["text_body"]};
    font-size: 1.25rem;
    line-height: 1;
    font-weight: 900;
    margin-bottom: 6px;
}}

.defence-detail-label {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.70rem;
    font-weight: 750;
    text-align: center;
    line-height: 1.15;
}}

@media (max-width: 1100px) {{
    .defence-main-grid {{
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }}

    .defence-rate-grid,
    .defence-detail-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}

    .defence-detail-card:nth-child(4n) {{
        border-right: 1px solid rgba(51, 65, 85, 0.85);
    }}

    .defence-detail-card:nth-child(2n) {{
        border-right: none;
    }}
}}

@media (max-width: 700px) {{
    .defence-rate-grid,
    .defence-detail-grid {{
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }}

    .defence-detail-card {{
        border-right: none;
    }}
}}

# CIRCLE
.circle-rate-card {{
    background: {BRAND_COLORS["background_card"]};
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    padding: 14px;
    text-align: center;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.circle-rate-title {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.82rem;
    font-weight: 850;
    margin-bottom: 12px;
    text-align: center;
    width: 100%;
}}

.circle-rate {{
    width: 132px;
    height: 132px;
    margin: 0 auto;
    border-radius: 50%;
    background:
        conic-gradient(
            {BRAND_COLORS["accent"]} calc(var(--value) * 1%),
            rgba(203, 213, 225, 0.14) 0
        );

    display: flex;
    align-items: center;
    justify-content: center;
}}

.circle-rate-inner {{
    width: 96px;
    height: 96px;
    border-radius: 50%;
    background: {BRAND_COLORS["background_card"]};

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}}

.circle-rate-value {{
    color: {BRAND_COLORS["text_body"]};
    font-size: 1.35rem;
    font-weight: 900;
    line-height: 1;
    text-align: center;
}}

.circle-rate-label {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.68rem;
    font-weight: 700;
    margin-top: 5px;
    text-align: center;
}}

.circle-rate-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
}}
# CIRCLE

.chart-section-header {{
    margin-top: 4px;
    margin-bottom: 16px;
}}

.chart-section-title {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 1.05rem;
    font-weight: 850;
}}

.chart-section-description {{
    color: {BRAND_COLORS["text_muted"]};
    font-size: 0.78rem;
    margin-top: 4px;
}}

/* =========================
   Player Goalkeeping Panel
========================= */

.goalkeeping-panel {{
    background: rgba(30, 41, 59, 0.62);
    border: 1px solid {BRAND_COLORS["border"]};
    border-radius: 16px;
    padding: 16px;
    margin-top: 8px;
}}

.goalkeeping-panel-title {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 1.05rem;
    font-weight: 850;
    margin-bottom: 4px;
}}

.goalkeeping-panel-description {{
    color: {BRAND_COLORS["text_muted"]};
    font-size: 0.78rem;
    margin-bottom: 14px;
}}

.goalkeeping-main-grid {{
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 14px;
    margin-bottom: 14px;
}}

.goalkeeping-box {{
    background: {BRAND_COLORS["background_card"]};
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    padding: 14px;
}}

.goalkeeping-box-title {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.82rem;
    font-weight: 850;
    margin-bottom: 12px;
}}

.goalkeeping-detail-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    overflow: hidden;
}}

.goalkeeping-detail-card {{
    background: {BRAND_COLORS["background_card"]};
    border-right: 1px solid rgba(51, 65, 85, 0.85);
    border-bottom: 1px solid rgba(51, 65, 85, 0.85);
    padding: 13px 10px;
    min-height: 86px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.goalkeeping-detail-card:nth-child(3n) {{
    border-right: none;
}}

.goalkeeping-detail-value {{
    color: {BRAND_COLORS["text_body"]};
    font-size: 1.35rem;
    line-height: 1;
    font-weight: 900;
    margin-bottom: 6px;
}}

.goalkeeping-detail-label {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.70rem;
    font-weight: 750;
    text-align: center;
    line-height: 1.15;
}}

.goalkeeping-secondary-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    border: 1px solid rgba(51, 65, 85, 0.85);
    border-radius: 14px;
    overflow: hidden;
}}

.goalkeeping-secondary-card {{
    background: {BRAND_COLORS["background_card"]};
    border-right: 1px solid rgba(51, 65, 85, 0.85);
    border-bottom: 1px solid rgba(51, 65, 85, 0.85);
    padding: 13px 10px;
    min-height: 78px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.goalkeeping-secondary-card:nth-child(4n) {{
    border-right: none;
}}

.goalkeeping-secondary-value {{
    color: {BRAND_COLORS["text_body"]};
    font-size: 1.25rem;
    line-height: 1;
    font-weight: 900;
    margin-bottom: 6px;
}}

.goalkeeping-secondary-label {{
    color: {BRAND_COLORS["text_main"]};
    font-size: 0.70rem;
    font-weight: 750;
    text-align: center;
    line-height: 1.15;
}}

@media (max-width: 1100px) {{
    .goalkeeping-main-grid {{
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }}

    .goalkeeping-detail-grid,
    .goalkeeping-secondary-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}

    .goalkeeping-detail-card:nth-child(3n),
    .goalkeeping-secondary-card:nth-child(4n) {{
        border-right: 1px solid rgba(51, 65, 85, 0.85);
    }}

    .goalkeeping-detail-card:nth-child(2n),
    .goalkeeping-secondary-card:nth-child(2n) {{
        border-right: none;
    }}
}}

@media (max-width: 700px) {{
    .goalkeeping-detail-grid,
    .goalkeeping-secondary-grid {{
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }}

    .goalkeeping-detail-card,
    .goalkeeping-secondary-card {{
        border-right: none;
    }}
}}

/* =========================
   Player Ratings List
========================= */

.rating-list-title {{
    color: #E2E8F0;
    font-size: 1.75rem;
    line-height: 1.15;
    font-weight: 850;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

/* Main container */
.rating-list-container {{
    width: 100%;
    border: 1px solid #475569;
    border-radius: 12px;
    overflow: hidden;
    background: rgba(15, 23, 42, 0.72);
    margin-top: 1rem;
}}

/* Header row */
.rating-list-header {{
    display: grid;
    align-items: center;
    min-height: 48px;
    background: rgba(30, 41, 59, 0.82);
    border-bottom: 1px solid rgba(71, 85, 105, 0.70);
}}

/* Body rows */
.rating-list-row {{
    display: grid;
    align-items: center;
    min-height: 48px;
    border-bottom: 1px solid rgba(71, 85, 105, 0.35);
    transition:
        background 0.15s ease,
        border-color 0.15s ease;
}}

.rating-list-row:last-child {{
    border-bottom: none;
}}

.rating-list-row:hover {{
    background: rgba(51, 65, 85, 0.55);
}}

/* Header cells */
.rating-list-header-cell {{
    color: #CBD5E1;
    font-size: 0.86rem;
    line-height: 1.2;
    font-weight: 850;
    padding: 0.75rem 0.85rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

/* Body cells */
.rating-list-cell {{
    color: #E2E8F0;
    font-size: 0.88rem;
    line-height: 1.2;
    font-weight: 750;
    padding: 0.78rem 0.85rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}

/* Alignment */
.rating-list-cell.align-left,
.rating-list-header-cell.align-left {{
    text-align: left;
}}

.rating-list-cell.align-center,
.rating-list-header-cell.align-center {{
    text-align: center;
}}

.rating-list-cell.align-right,
.rating-list-header-cell.align-right {{
    text-align: right;
}}

/* Special cells */
.rating-list-cell.is-rank {{
    color: #CBD5E1;
    font-weight: 850;
}}

.rating-list-cell.is-player {{
    font-weight: 900;
}}

.rating-list-cell.is-rating {{
    font-variant-numeric: tabular-nums;
}}

.rating-list-cell.is-overall {{
    color: #E2E8F0;
    font-weight: 950;
}}

.rating-list-header-cell.is-overall {{
    color: #CBD5E1;
    font-weight: 950;
}}

/* Empty state */
.rating-list-empty {{
    color: #94A3B8;
    font-size: 0.9rem;
    padding: 1rem;
    border: 1px solid #475569;
    border-radius: 12px;
    background: rgba(30, 41, 59, 0.50);
}}

/* =========================
   Sort Controls
========================= */

.rating-sort-controls {{
    margin-bottom: 0.75rem;
}}

/* Keep Streamlit controls compact around ratings table */
div[data-testid="stSelectbox"] label,
div[data-testid="stSegmentedControl"] label {{
    color: #CBD5E1;
    font-size: 0.82rem;
}}

/* =========================
   Responsive behavior
========================= */

@media (max-width: 1400px) {{
    .rating-list-container {{
        overflow-x: auto;
        overflow-y: hidden;
    }}

    .rating-list-header,
    .rating-list-row {{
        min-width: 1100px;
    }}
}}

@media (max-width: 1100px) {{
    .rating-list-title {{
        font-size: 1.45rem;
    }}

    .rating-list-header,
    .rating-list-row {{
        min-width: 1040px;
    }}

    .rating-list-header-cell {{
        font-size: 0.80rem;
        padding: 0.70rem 0.75rem;
    }}

    .rating-list-cell {{
        font-size: 0.82rem;
        padding: 0.72rem 0.75rem;
    }}
}}

@media (max-width: 800px) {{
    .rating-list-title {{
        font-size: 1.30rem;
    }}

    .rating-list-container {{
        border-radius: 10px;
    }}

    .rating-list-header,
    .rating-list-row {{
        min-width: 980px;
    }}

    .rating-list-header {{
        min-height: 44px;
    }}

    .rating-list-row {{
        min-height: 46px;
    }}

    .rating-list-header-cell {{
        font-size: 0.76rem;
        padding: 0.65rem 0.70rem;
    }}

    .rating-list-cell {{
        font-size: 0.78rem;
        padding: 0.68rem 0.70rem;
    }}
}}

@media (max-width: 600px) {{
    .rating-list-title {{
        font-size: 1.18rem;
        margin-bottom: 0.75rem;
    }}

    .rating-list-header,
    .rating-list-row {{
        min-width: 940px;
    }}
}}

            @media (max-width: 700px) {{
                .player-profile-header-top {{
                    flex-direction: column;
                    align-items: flex-start;
                }}

                .player-profile-title {{
                    font-size: 1.85rem;
                }}

                .player-profile-season-row {{
                    max-width: 100%;
                }}
            }}


            /* =========================
               Responsive Layout
            ========================= */
            
            
            @media (max-width: 1400px) {{
                .player-bio-grid {{
                    grid-template-columns: repeat(4, minmax(0, 1fr));
                }}
            }}

            @media (max-width: 800px) {{
                .player-bio-grid {{
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }}
            }}

            @media (max-width: 1400px) {{
                .entity-grid {{
                    grid-template-columns: repeat(4, minmax(0, 1fr));
                }}
            }}

            @media (max-width: 900px) {{
                .entity-grid {{
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }}

                .player-list-wrapper {{
                    overflow-x: auto;
                }}

                .player-list-header,
                .player-list-row {{
                    min-width: 900px;
                }}
            }}

            @media (max-width: 600px) {{
                .entity-grid {{
                    grid-template-columns: repeat(1, minmax(0, 1fr));
                }}

                .team-header {{
                    padding: 22px 20px;
                }}

                .team-header-title {{
                    font-size: 2rem;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )