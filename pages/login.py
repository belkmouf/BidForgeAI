"""
Login page for BidForge AI
"""

import streamlit as st
from utils.auth import login_user


def render():
    """Render the login page"""

    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Hero section
        st.markdown("""
            <div style='text-align: center; padding: 3rem 0 2rem 0;'>
                <h1 style='color: #b8995a; font-size: 3.5rem; margin: 0; font-weight: 800;
                           font-family: "Syne", sans-serif; letter-spacing: -1px;'>
                    ⚡ BidForge AI
                </h1>
                <p style='color: #0d7377; font-size: 1.3rem; margin: 1rem 0 0 0; font-weight: 600;
                          font-family: "Inter", sans-serif;'>
                    Construction Bidding Excellence
                </p>
                <div style='height: 3px; background: linear-gradient(90deg, transparent 0%, #0d7377 20%, #b8995a 50%, #0d7377 80%, transparent 100%);
                            margin: 2rem auto; max-width: 300px; border-radius: 2px;'></div>
                <p style='color: rgba(255,255,255,0.7); font-size: 1rem; margin-top: 1rem;'>
                    AI-Powered Proposal Automation for GCC Construction Leaders
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Login card
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(13, 115, 119, 0.1) 100%);
                        border: 1px solid rgba(184, 153, 90, 0.3);
                        border-radius: 20px;
                        padding: 3rem;
                        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
                        backdrop-filter: blur(10px);
                        margin: 2rem 0;'>
                <h3 style='color: #ffffff; text-align: center; margin-bottom: 2rem; font-size: 1.5rem;
                           font-family: "Syne", sans-serif;'>
                    Welcome Back
                </h3>
            </div>
        """, unsafe_allow_html=True)

        # Login form
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "Email Address",
                placeholder="your.email@company.com",
                help="Enter your registered email address"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••",
                help="Enter your password"
            )

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                login_button = st.form_submit_button("🔐 Sign In", use_container_width=True, type="primary")
            with col_btn2:
                demo_button = st.form_submit_button("✨ Demo Login", use_container_width=True, type="secondary")

            if login_button:
                if not email or not password:
                    st.error("⚠️ Please enter both email and password")
                else:
                    with st.spinner("Authenticating..."):
                        if login_user(email, password):
                            st.success("✅ Login successful! Redirecting...")
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password")

            if demo_button:
                # Auto-fill demo credentials
                if login_user('admin@bidforge.ai', 'Admin@123'):
                    st.success("✅ Demo login successful!")
                    st.rerun()

        # Demo credentials info
        st.markdown("""
            <div style='background: rgba(13, 115, 119, 0.1);
                        border: 1px solid rgba(13, 115, 119, 0.3);
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin-top: 2rem;'>
                <h4 style='color: #b8995a; margin: 0 0 1rem 0; font-size: 0.9rem;
                           text-transform: uppercase; letter-spacing: 1px;'>
                    🎯 Demo Accounts
                </h4>
                <div style='color: rgba(255,255,255,0.85); font-size: 0.85rem; line-height: 1.8;'>
                    <strong style='color: #0d7377;'>Administrator:</strong><br>
                    📧 admin@bidforge.ai | 🔑 Admin@123<br><br>

                    <strong style='color: #0d7377;'>Project Manager:</strong><br>
                    📧 manager@bidforge.ai | 🔑 Manager@123<br><br>

                    <strong style='color: #0d7377;'>Regular User:</strong><br>
                    📧 user@bidforge.ai | 🔑 User@123
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Features showcase
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center;'>
                <h4 style='color: #b8995a; font-size: 1.1rem; margin-bottom: 1.5rem;'>
                    🚀 Powered by Advanced AI
                </h4>
                <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;'>
                    <div style='padding: 1rem; background: rgba(13, 115, 119, 0.1);
                                border-radius: 10px; border: 1px solid rgba(13, 115, 119, 0.2);'>
                        <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>🤖</div>
                        <div style='color: #e0e0e0; font-size: 0.8rem; font-weight: 600;'>Multi-AI Engine</div>
                    </div>
                    <div style='padding: 1rem; background: rgba(184, 153, 90, 0.1);
                                border-radius: 10px; border: 1px solid rgba(184, 153, 90, 0.2);'>
                        <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>📊</div>
                        <div style='color: #e0e0e0; font-size: 0.8rem; font-weight: 600;'>Smart Analytics</div>
                    </div>
                    <div style='padding: 1rem; background: rgba(13, 115, 119, 0.1);
                                border-radius: 10px; border: 1px solid rgba(13, 115, 119, 0.2);'>
                        <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>⚡</div>
                        <div style='color: #e0e0e0; font-size: 0.8rem; font-weight: 600;'>Instant Results</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Footer
        st.markdown("""
            <div style='text-align: center; margin-top: 3rem; padding-top: 2rem;
                        border-top: 1px solid rgba(184, 153, 90, 0.2);'>
                <p style='color: rgba(255,255,255,0.5); font-size: 0.8rem;'>
                    © 2025 BidForge AI. Premium Construction Bidding Automation.
                </p>
            </div>
        """, unsafe_allow_html=True)
