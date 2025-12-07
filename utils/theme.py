"""
GCC-Inspired Premium Theme for BidForge AI
Colors: Deep Teal (#0d7377), Antique Gold (#b8995a), Charcoal (#1a1a1a)
"""

import streamlit as st


def apply_gcc_theme():
    """Apply the premium GCC-inspired theme with custom CSS"""

    st.markdown("""
        <style>
        /* Import premium fonts */
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600;700&family=Fraunces:wght@300;400;600;700&display=swap');

        /* Root variables - GCC Color Palette */
        :root {
            --charcoal: #1a1a1a;
            --deep-teal: #0d7377;
            --deep-teal-dark: #0a5a5d;
            --deep-teal-light: #14a0a6;
            --antique-gold: #b8995a;
            --antique-gold-light: #d4b676;
            --antique-gold-dark: #9a7e47;
            --white: #ffffff;
            --light-gray: #f5f5f5;
            --medium-gray: #e0e0e0;
            --dark-gray: #2a2a2a;
        }

        /* Main app background with subtle gradient */
        .stApp {
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #0f0f0f 100%);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%);
            border-right: 1px solid rgba(184, 153, 90, 0.15);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #e0e0e0;
        }

        /* Headers with premium styling */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Syne', sans-serif;
            color: #ffffff;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #ffffff 0%, #b8995a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
        }

        h2 {
            color: #b8995a;
            font-size: 1.8rem;
            border-bottom: 2px solid #0d7377;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
        }

        h3 {
            color: #0d7377;
            font-size: 1.4rem;
        }

        /* Card styling with premium effects */
        .element-container {
            transition: all 0.3s ease;
        }

        /* Metrics cards */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #b8995a;
            font-family: 'Syne', sans-serif;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.9rem;
            color: #e0e0e0;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        [data-testid="stMetricDelta"] {
            font-size: 0.85rem;
        }

        /* Buttons - Primary (Teal) */
        .stButton > button {
            background: linear-gradient(135deg, #0d7377 0%, #0a5a5d 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(13, 115, 119, 0.3);
            font-family: 'Inter', sans-serif;
            letter-spacing: 0.3px;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #14a0a6 0%, #0d7377 100%);
            box-shadow: 0 6px 20px rgba(13, 115, 119, 0.5);
            transform: translateY(-2px);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* Secondary buttons (Gold accent) */
        .stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, #b8995a 0%, #9a7e47 100%);
            box-shadow: 0 4px 12px rgba(184, 153, 90, 0.3);
        }

        .stButton > button[kind="secondary"]:hover {
            background: linear-gradient(135deg, #d4b676 0%, #b8995a 100%);
            box-shadow: 0 6px 20px rgba(184, 153, 90, 0.5);
        }

        /* Input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            background-color: rgba(26, 26, 26, 0.6);
            border: 1px solid rgba(184, 153, 90, 0.3);
            border-radius: 8px;
            color: #ffffff;
            padding: 0.75rem;
            font-family: 'Inter', sans-serif;
            transition: all 0.3s ease;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #0d7377;
            box-shadow: 0 0 0 2px rgba(13, 115, 119, 0.2);
        }

        /* File uploader */
        [data-testid="stFileUploader"] {
            background: linear-gradient(135deg, rgba(13, 115, 119, 0.1) 0%, rgba(26, 26, 26, 0.6) 100%);
            border: 2px dashed rgba(184, 153, 90, 0.5);
            border-radius: 12px;
            padding: 2rem;
            transition: all 0.3s ease;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: #0d7377;
            background: linear-gradient(135deg, rgba(13, 115, 119, 0.2) 0%, rgba(26, 26, 26, 0.6) 100%);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(26, 26, 26, 0.6);
            border-radius: 10px;
            padding: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 8px;
            color: #e0e0e0;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            font-family: 'Inter', sans-serif;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #0d7377 0%, #0a5a5d 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(13, 115, 119, 0.4);
        }

        /* Expander */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, rgba(13, 115, 119, 0.15) 0%, rgba(26, 26, 26, 0.6) 100%);
            border: 1px solid rgba(184, 153, 90, 0.2);
            border-radius: 10px;
            color: #b8995a;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            padding: 1rem;
        }

        .streamlit-expanderHeader:hover {
            background: linear-gradient(135deg, rgba(13, 115, 119, 0.25) 0%, rgba(26, 26, 26, 0.6) 100%);
            border-color: #0d7377;
        }

        /* Dataframe/Table */
        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        /* Progress bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #0d7377 0%, #b8995a 100%);
        }

        /* Spinner */
        .stSpinner > div {
            border-top-color: #0d7377;
        }

        /* Success/Info/Warning/Error messages */
        .stAlert {
            border-radius: 10px;
            border-left-width: 4px;
            font-family: 'Inter', sans-serif;
        }

        [data-baseweb="notification"][kind="success"] {
            background-color: rgba(13, 115, 119, 0.1);
            border-left-color: #0d7377;
        }

        [data-baseweb="notification"][kind="info"] {
            background-color: rgba(184, 153, 90, 0.1);
            border-left-color: #b8995a;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #1a1a1a;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #0d7377 0%, #b8995a 100%);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #14a0a6 0%, #d4b676 100%);
        }

        /* Custom card component */
        .premium-card {
            background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(13, 115, 119, 0.05) 100%);
            border: 1px solid rgba(184, 153, 90, 0.2);
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
        }

        .premium-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(13, 115, 119, 0.3);
            border-color: #0d7377;
        }

        /* Stats badge */
        .stats-badge {
            display: inline-block;
            background: linear-gradient(135deg, #0d7377 0%, #0a5a5d 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            margin: 0.25rem;
            box-shadow: 0 2px 8px rgba(13, 115, 119, 0.3);
        }

        /* Risk indicators */
        .risk-low {
            color: #4ade80;
            font-weight: 700;
        }

        .risk-medium {
            color: #fbbf24;
            font-weight: 700;
        }

        .risk-high {
            color: #f87171;
            font-weight: 700;
        }

        .risk-critical {
            color: #dc2626;
            font-weight: 700;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        /* Loading animation */
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }

        .loading-shimmer {
            animation: shimmer 2s infinite;
            background: linear-gradient(90deg, #1a1a1a 0%, #0d7377 50%, #1a1a1a 100%);
            background-size: 1000px 100%;
        }

        /* Premium divider */
        .premium-divider {
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, #0d7377 50%, transparent 100%);
            margin: 2rem 0;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)


def create_card(content: str, hover_effect: bool = True) -> str:
    """Create a premium styled card"""
    return f"""
        <div class="premium-card" style="{'cursor: pointer;' if hover_effect else ''}">
            {content}
        </div>
    """


def create_stat_badge(label: str, value: str, color: str = "teal") -> str:
    """Create a stat badge"""
    color_map = {
        "teal": "linear-gradient(135deg, #0d7377 0%, #0a5a5d 100%)",
        "gold": "linear-gradient(135deg, #b8995a 0%, #9a7e47 100%)",
        "gray": "linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%)"
    }
    bg = color_map.get(color, color_map["teal"])

    return f"""
        <div style="display: inline-block; background: {bg}; color: white;
                    padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;
                    font-size: 0.85rem; margin: 0.25rem;
                    box-shadow: 0 2px 8px rgba(13, 115, 119, 0.3);">
            <span style="opacity: 0.8; font-size: 0.75rem;">{label}</span>
            <span style="margin-left: 0.5rem; font-size: 1rem;">{value}</span>
        </div>
    """


def create_section_header(title: str, subtitle: str = "") -> str:
    """Create a premium section header"""
    return f"""
        <div style="margin: 2rem 0 1.5rem 0;">
            <h2 style="color: #b8995a; font-size: 1.8rem; margin: 0; font-family: 'Syne', sans-serif;
                       font-weight: 700; letter-spacing: -0.5px;">
                {title}
            </h2>
            {f'<p style="color: #e0e0e0; font-size: 0.95rem; margin: 0.5rem 0 0 0; opacity: 0.8;">{subtitle}</p>' if subtitle else ''}
            <div style="height: 2px; background: linear-gradient(90deg, #0d7377 0%, transparent 100%);
                        margin-top: 1rem;"></div>
        </div>
    """


def get_risk_color(risk_level: str) -> str:
    """Get color for risk level"""
    risk_colors = {
        "Low": "#4ade80",
        "Medium": "#fbbf24",
        "High": "#f87171",
        "Critical": "#dc2626"
    }
    return risk_colors.get(risk_level, "#e0e0e0")


def create_premium_divider():
    """Create a premium styled divider"""
    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)
