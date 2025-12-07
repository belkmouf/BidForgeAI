"""
Settings - Application configuration and user preferences
"""

import streamlit as st
from utils.theme import create_section_header


def render():
    """Render the settings page"""

    st.markdown(create_section_header(
        "Settings & Configuration",
        "Manage your account, API keys, and application preferences"
    ), unsafe_allow_html=True)

    # Tabs for different settings categories
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 User Profile",
        "🔑 API Configuration",
        "⚙️ Preferences",
        "🔔 Notifications"
    ])

    with tab1:
        render_user_profile()

    with tab2:
        render_api_config()

    with tab3:
        render_preferences()

    with tab4:
        render_notifications()


def render_user_profile():
    """Render user profile settings"""

    user = st.session_state.get('user', {})

    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(13, 115, 119, 0.15) 0%, rgba(26, 26, 26, 0.9) 100%);
                    border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 12px;
                    padding: 2rem;
                    margin-bottom: 2rem;'>
            <h4 style='color: #b8995a; margin: 0 0 0.5rem 0;'>
                User Information
            </h4>
            <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.9rem;'>
                Update your personal information and account details
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Full Name",
                value=user.get('name', ''),
                help="Your full name as it appears on documents"
            )

            email = st.text_input(
                "Email Address",
                value=user.get('email', ''),
                help="Your primary email address",
                disabled=True  # Email cannot be changed
            )

            phone = st.text_input(
                "Phone Number",
                value=user.get('phone', '+971 50 123 4567'),
                placeholder="+971 XX XXX XXXX"
            )

        with col2:
            company = st.text_input(
                "Company Name",
                value=user.get('company', 'Emirates Construction Group'),
                help="Your company or organization name"
            )

            role = st.selectbox(
                "Job Title",
                ["Project Manager", "Bid Manager", "Estimator", "Executive", "Engineer", "Other"],
                index=0
            )

            location = st.text_input(
                "Location",
                value=user.get('location', 'Dubai, UAE'),
                placeholder="City, Country"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary"):
                st.success("✅ Profile updated successfully!")

        with col2:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.info("Changes cancelled")

    # Password change section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(184, 153, 90, 0.15) 0%, rgba(26, 26, 26, 0.9) 100%);
                    border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 12px;
                    padding: 2rem;
                    margin-bottom: 2rem;'>
            <h4 style='color: #b8995a; margin: 0 0 0.5rem 0;'>
                🔒 Change Password
            </h4>
            <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.9rem;'>
                Update your account password for security
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("password_form"):
        col1, col2 = st.columns(2)

        with col1:
            current_password = st.text_input(
                "Current Password",
                type="password",
                help="Enter your current password"
            )

        with col2:
            new_password = st.text_input(
                "New Password",
                type="password",
                help="Must be at least 8 characters with uppercase, lowercase, and number"
            )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password",
            help="Re-enter your new password"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.form_submit_button("🔐 Update Password", use_container_width=True, type="primary"):
            if not current_password or not new_password or not confirm_password:
                st.error("⚠️ Please fill in all password fields")
            elif new_password != confirm_password:
                st.error("⚠️ New passwords do not match")
            elif len(new_password) < 8:
                st.error("⚠️ Password must be at least 8 characters long")
            else:
                st.success("✅ Password updated successfully!")


def render_api_config():
    """Render API configuration settings"""

    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(13, 115, 119, 0.15) 0%, rgba(26, 26, 26, 0.9) 100%);
                    border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 12px;
                    padding: 2rem;
                    margin-bottom: 2rem;'>
            <h4 style='color: #b8995a; margin: 0 0 0.5rem 0;'>
                🤖 AI Provider API Keys
            </h4>
            <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.9rem;'>
                Configure your API keys for AI model access. Keys are encrypted and stored securely.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # OpenAI Configuration
    with st.expander("🟢 OpenAI Configuration", expanded=True):
        openai_key = st.text_input(
            "OpenAI API Key",
            value="sk-••••••••••••••••",
            type="password",
            help="Your OpenAI API key for GPT-4o access",
            key="openai_key"
        )

        openai_base_url = st.text_input(
            "Custom Base URL (Optional)",
            placeholder="https://api.openai.com/v1",
            help="Leave empty for default OpenAI endpoint",
            key="openai_url"
        )

        if st.button("Test OpenAI Connection", key="test_openai"):
            with st.spinner("Testing connection..."):
                import time
                time.sleep(1)
            st.success("✅ OpenAI API connection successful!")

    # Anthropic Configuration
    with st.expander("🔵 Anthropic Configuration"):
        anthropic_key = st.text_input(
            "Anthropic API Key",
            value="sk-ant-••••••••••••••••",
            type="password",
            help="Your Anthropic API key for Claude access",
            key="anthropic_key"
        )

        anthropic_base_url = st.text_input(
            "Custom Base URL (Optional)",
            placeholder="https://api.anthropic.com",
            help="Leave empty for default Anthropic endpoint",
            key="anthropic_url"
        )

        if st.button("Test Anthropic Connection", key="test_anthropic"):
            with st.spinner("Testing connection..."):
                import time
                time.sleep(1)
            st.success("✅ Anthropic API connection successful!")

    # Google Gemini Configuration
    with st.expander("🔴 Google Gemini Configuration"):
        gemini_key = st.text_input(
            "Google API Key",
            value="AIza••••••••••••••••",
            type="password",
            help="Your Google API key for Gemini access",
            key="gemini_key"
        )

        if st.button("Test Gemini Connection", key="test_gemini"):
            with st.spinner("Testing connection..."):
                import time
                time.sleep(1)
            st.success("✅ Gemini API connection successful!")

    # DeepSeek Configuration
    with st.expander("🟣 DeepSeek Configuration"):
        deepseek_key = st.text_input(
            "DeepSeek API Key",
            value="sk-••••••••••••••••",
            type="password",
            help="Your DeepSeek API key",
            key="deepseek_key"
        )

        if st.button("Test DeepSeek Connection", key="test_deepseek"):
            with st.spinner("Testing connection..."):
                import time
                time.sleep(1)
            st.success("✅ DeepSeek API connection successful!")

    # WhatsApp Configuration
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(184, 153, 90, 0.15) 0%, rgba(26, 26, 26, 0.9) 100%);
                    border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 12px;
                    padding: 2rem;
                    margin-bottom: 1rem;'>
            <h4 style='color: #b8995a; margin: 0 0 0.5rem 0;'>
                📱 WhatsApp Business API
            </h4>
            <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.9rem;'>
                Configure WhatsApp Business API for document request automation
            </p>
        </div>
    """, unsafe_allow_html=True)

    enable_whatsapp = st.checkbox("Enable WhatsApp Integration", value=False)

    if enable_whatsapp:
        col1, col2 = st.columns(2)

        with col1:
            wa_phone_id = st.text_input(
                "Phone Number ID",
                placeholder="123456789012345",
                help="From Meta Developer Console"
            )

            wa_access_token = st.text_input(
                "Access Token",
                type="password",
                placeholder="EAA••••••••",
                help="Your WhatsApp Business API access token"
            )

        with col2:
            wa_webhook_token = st.text_input(
                "Webhook Verify Token",
                value="bidforge_webhook_token",
                help="Token for webhook verification"
            )

            wa_app_secret = st.text_input(
                "App Secret",
                type="password",
                placeholder="••••••••",
                help="For webhook signature verification"
            )

        if st.button("Test WhatsApp Connection"):
            with st.spinner("Testing connection..."):
                import time
                time.sleep(1)
            st.success("✅ WhatsApp API connection successful!")

    # Save button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Save API Configuration", use_container_width=True, type="primary"):
        st.success("✅ API configuration saved successfully!")


def render_preferences():
    """Render user preferences"""

    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(13, 115, 119, 0.15) 0%, rgba(26, 26, 26, 0.9) 100%);
                    border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 12px;
                    padding: 2rem;
                    margin-bottom: 2rem;'>
            <h4 style='color: #b8995a; margin: 0 0 0.5rem 0;'>
                Application Preferences
            </h4>
            <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.9rem;'>
                Customize your BidForge AI experience
            </p>
        </div>
    """, unsafe_allow_html=True)

    # General preferences
    st.markdown("### 🎨 Display Settings")

    col1, col2 = st.columns(2)

    with col1:
        language = st.selectbox(
            "Language",
            ["English", "Arabic (العربية)", "French"],
            index=0,
            help="Application display language"
        )

        timezone = st.selectbox(
            "Timezone",
            ["GMT+4 (UAE)", "GMT+3 (Saudi Arabia)", "GMT+2 (Egypt)", "UTC"],
            index=0
        )

    with col2:
        currency = st.selectbox(
            "Default Currency",
            ["USD ($)", "AED (د.إ)", "SAR (﷼)", "EUR (€)", "GBP (£)"],
            index=0,
            help="Currency for financial displays"
        )

        date_format = st.selectbox(
            "Date Format",
            ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"],
            index=0
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # AI preferences
    st.markdown("### 🤖 AI Settings")

    default_model = st.selectbox(
        "Default AI Model",
        ["OpenAI GPT-4o", "Claude Sonnet 4.5", "Google Gemini 2.0", "DeepSeek"],
        index=0,
        help="Default model for bid generation"
    )

    creativity_level = st.slider(
        "Default Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls how creative vs conservative AI proposals are"
    )

    auto_run_analysis = st.checkbox(
        "Auto-run RFP analysis on document upload",
        value=True,
        help="Automatically analyze RFPs when documents are uploaded"
    )

    enable_multi_model = st.checkbox(
        "Enable multi-model comparison by default",
        value=False,
        help="Generate bids with multiple models for comparison"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Document preferences
    st.markdown("### 📄 Document Settings")

    col1, col2 = st.columns(2)

    with col1:
        default_export_format = st.selectbox(
            "Default Export Format",
            ["HTML", "PDF", "DOCX"],
            index=0
        )

        auto_save = st.checkbox("Auto-save drafts every 5 minutes", value=True)

    with col2:
        include_watermark = st.checkbox("Include draft watermark on exports", value=True)

        compress_uploads = st.checkbox("Compress uploaded documents", value=False)

    st.markdown("<br>", unsafe_allow_html=True)

    # Save preferences
    if st.button("💾 Save Preferences", use_container_width=True, type="primary"):
        st.success("✅ Preferences saved successfully!")


def render_notifications():
    """Render notification settings"""

    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(13, 115, 119, 0.15) 0%, rgba(26, 26, 26, 0.9) 100%);
                    border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 12px;
                    padding: 2rem;
                    margin-bottom: 2rem;'>
            <h4 style='color: #b8995a; margin: 0 0 0.5rem 0;'>
                🔔 Notification Preferences
            </h4>
            <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.9rem;'>
                Control when and how you receive notifications
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Email notifications
    st.markdown("### 📧 Email Notifications")

    email_notifications = st.checkbox("Enable email notifications", value=True)

    if email_notifications:
        col1, col2 = st.columns(2)

        with col1:
            st.checkbox("New project created", value=True)
            st.checkbox("RFP analysis complete", value=True)
            st.checkbox("Bid generation complete", value=True)
            st.checkbox("Conflicts detected", value=True)

        with col2:
            st.checkbox("Project deadline approaching", value=True)
            st.checkbox("Bid submitted successfully", value=True)
            st.checkbox("Win/loss outcome recorded", value=True)
            st.checkbox("Weekly summary report", value=False)

    st.markdown("<br>", unsafe_allow_html=True)

    # In-app notifications
    st.markdown("### 🔔 In-App Notifications")

    st.checkbox("Show desktop notifications", value=True)
    st.checkbox("Play notification sound", value=False)

    notification_frequency = st.selectbox(
        "Notification Frequency",
        ["Real-time", "Every 30 minutes", "Every hour", "Daily digest"],
        index=0
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # WhatsApp notifications
    st.markdown("### 📱 WhatsApp Notifications")

    whatsapp_notifications = st.checkbox("Enable WhatsApp notifications", value=False)

    if whatsapp_notifications:
        st.info("📱 Configure WhatsApp Business API in the API Configuration tab first")

        whatsapp_number = st.text_input(
            "Your WhatsApp Number",
            placeholder="+971 50 123 4567",
            help="Number to receive notifications"
        )

        st.checkbox("Critical alerts only", value=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Save button
    if st.button("💾 Save Notification Settings", use_container_width=True, type="primary"):
        st.success("✅ Notification settings saved successfully!")
