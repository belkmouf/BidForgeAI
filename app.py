"""
BidForge AI - Construction Bidding Automation System
A premium Streamlit application for GCC construction companies
"""

import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Must be the first Streamlit command
st.set_page_config(
    page_title="BidForge AI - Construction Bidding Excellence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://bidforge.ai/support',
        'Report a bug': 'https://bidforge.ai/report',
        'About': "BidForge AI - Premium Construction Bidding Automation System"
    }
)

# Import page modules (will be created)
from pages import (
    dashboard,
    project_workspace,
    rfp_analysis,
    bid_generation,
    conflict_detection,
    win_probability,
    settings,
    login
)
from utils.auth import check_authentication
from utils.theme import apply_gcc_theme

# Apply GCC-inspired theme
apply_gcc_theme()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_project' not in st.session_state:
    st.session_state.current_project = None


def main():
    """Main application entry point"""

    # Check authentication
    if not st.session_state.authenticated:
        login.render()
        return

    # Sidebar navigation with premium styling
    with st.sidebar:
        # Logo and branding
        st.markdown("""
            <div style='text-align: center; padding: 1.5rem 0; border-bottom: 2px solid #0d7377;'>
                <h1 style='color: #b8995a; font-size: 2.2rem; margin: 0; font-weight: 700; letter-spacing: -0.5px;'>
                    ⚡ BidForge AI
                </h1>
                <p style='color: #0d7377; font-size: 0.85rem; margin: 0.5rem 0 0 0; font-weight: 500;'>
                    Construction Bidding Excellence
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # User info
        if st.session_state.user:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #0d7377 0%, #0a5a5d 100%);
                            padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem;
                            border: 1px solid rgba(184, 153, 90, 0.3);'>
                    <p style='color: #b8995a; font-size: 0.75rem; margin: 0; text-transform: uppercase;
                              letter-spacing: 1px; font-weight: 600;'>Welcome Back</p>
                    <p style='color: white; font-size: 1.1rem; margin: 0.3rem 0 0 0; font-weight: 600;'>
                        {st.session_state.user.get('name', 'User')}
                    </p>
                    <p style='color: rgba(255,255,255,0.7); font-size: 0.8rem; margin: 0.2rem 0 0 0;'>
                        {st.session_state.user.get('role', 'User')}
                    </p>
                </div>
            """, unsafe_allow_html=True)

        # Main navigation menu
        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "Projects",
                "RFP Analysis",
                "Bid Generation",
                "Conflict Detection",
                "Win Probability",
                "Settings"
            ],
            icons=[
                "speedometer2",
                "folder",
                "file-earmark-text",
                "file-earmark-richtext",
                "exclamation-triangle",
                "graph-up-arrow",
                "gear"
            ],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent"
                },
                "icon": {
                    "color": "#b8995a",
                    "font-size": "1.1rem"
                },
                "nav-link": {
                    "font-size": "0.95rem",
                    "text-align": "left",
                    "margin": "0.3rem 0",
                    "padding": "0.75rem 1rem",
                    "border-radius": "10px",
                    "color": "#e0e0e0",
                    "background-color": "transparent",
                    "font-weight": "500",
                    "transition": "all 0.3s ease"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #0d7377 0%, #0a5a5d 100%)",
                    "color": "white",
                    "font-weight": "600",
                    "border-left": "4px solid #b8995a",
                    "box-shadow": "0 4px 12px rgba(13, 115, 119, 0.4)"
                },
                "nav-link:hover": {
                    "background-color": "rgba(13, 115, 119, 0.1)"
                }
            }
        )

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Quick stats in sidebar
        st.markdown("""
            <div style='background: rgba(26, 26, 26, 0.6); padding: 1rem; border-radius: 12px;
                        border: 1px solid rgba(184, 153, 90, 0.2);'>
                <p style='color: #b8995a; font-size: 0.7rem; margin: 0; text-transform: uppercase;
                          letter-spacing: 1px; font-weight: 600;'>Quick Stats</p>
            </div>
        """, unsafe_allow_html=True)

        # Logout button at bottom
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()

    # Main content area - Route to selected page
    if selected == "Dashboard":
        dashboard.render()
    elif selected == "Projects":
        project_workspace.render()
    elif selected == "RFP Analysis":
        rfp_analysis.render()
    elif selected == "Bid Generation":
        bid_generation.render()
    elif selected == "Conflict Detection":
        conflict_detection.render()
    elif selected == "Win Probability":
        win_probability.render()
    elif selected == "Settings":
        settings.render()


if __name__ == "__main__":
    main()
