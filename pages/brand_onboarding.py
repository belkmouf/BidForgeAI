"""
Brand Setup Onboarding for BidForge AI
Quick-start company and brand configuration
"""

import streamlit as st
import re
from datetime import datetime
from utils.database import db
from utils.theme import apply_theme


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}.*$'
    return re.match(pattern, url) is not None


def validate_hex_color(color: str) -> bool:
    """Validate HEX color format"""
    pattern = r'^#[0-9A-Fa-f]{6}$'
    return re.match(pattern, color) is not None


def generate_complementary_colors(primary_hex: str) -> dict:
    """Generate complementary accent and text colors based on primary brand color"""
    # Remove # if present
    hex_color = primary_hex.lstrip('#')

    # Convert to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # Calculate brightness (0-255)
    brightness = (r * 299 + g * 587 + b * 114) / 1000

    # Generate accent color (slightly lighter/darker version)
    accent_r = min(255, int(r * 1.2)) if brightness < 128 else max(0, int(r * 0.8))
    accent_g = min(255, int(g * 1.2)) if brightness < 128 else max(0, int(g * 0.8))
    accent_b = min(255, int(b * 1.2)) if brightness < 128 else max(0, int(b * 0.8))

    accent_hex = f"#{accent_r:02x}{accent_g:02x}{accent_b:02x}"

    # Text color based on background brightness
    text_color = "#FFFFFF" if brightness < 128 else "#1A1A1A"
    secondary_text = "#E0E0E0" if brightness < 128 else "#666666"

    return {
        'primary': primary_hex,
        'accent': accent_hex,
        'text': text_color,
        'secondary_text': secondary_text
    }


def main():
    # Apply theme
    apply_theme()

    st.markdown("""
        <h1 style='text-align: center; color: #C5A572; margin-bottom: 10px;'>
            🚀 Quick-Start Brand Setup
        </h1>
        <p style='text-align: center; color: #666; margin-bottom: 30px;'>
            <strong>Time: 5 Minutes</strong> | Goal: Configure your essential proposal branding
        </p>
    """, unsafe_allow_html=True)

    # Progress indicator
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1

    # Initialize form data
    if 'brand_data' not in st.session_state:
        st.session_state.brand_data = {}

    # Create form
    with st.form("brand_onboarding_form"):
        st.markdown("---")

        # SECTION 1: Company Basics
        st.markdown("### 📋 1. Company Basics")
        st.caption("Required for legal validity on cover pages and footers.")

        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input(
                "Company Name*",
                placeholder="e.g., Acme Corporation Ltd.",
                help="As it should appear on contracts",
                value=st.session_state.brand_data.get('company_name', '')
            )

            website_url = st.text_input(
                "Website URL*",
                placeholder="https://www.yourcompany.com",
                value=st.session_state.brand_data.get('website_url', '')
            )

        with col2:
            contact_email = st.text_input(
                "Proposal Contact Email*",
                placeholder="proposals@yourcompany.com",
                help="Where replies should be sent",
                value=st.session_state.brand_data.get('contact_email', '')
            )

            phone = st.text_input(
                "Contact Phone Number",
                placeholder="+1 (555) 123-4567",
                value=st.session_state.brand_data.get('phone', '')
            )

        hq_address = st.text_area(
            "Headquarters Address*",
            placeholder="123 Business Street, Suite 100\nCity, State ZIP\nCountry",
            help="Full physical address",
            height=100,
            value=st.session_state.brand_data.get('hq_address', '')
        )

        st.markdown("---")

        # SECTION 2: Visual Identity
        st.markdown("### 🎨 2. Visual Identity")
        st.caption("We will use these assets to auto-theme your entire document.")

        col1, col2 = st.columns([2, 1])

        with col1:
            logo_file = st.file_uploader(
                "Company Logo*",
                type=['png', 'svg', 'jpg', 'jpeg'],
                help="Upload: PNG or SVG (Transparent background recommended)",
                key="logo_uploader"
            )

            if logo_file is not None:
                st.image(logo_file, width=200, caption="Logo Preview")

        with col2:
            primary_color = st.color_picker(
                "Primary Brand Color*",
                value=st.session_state.brand_data.get('primary_color', '#0055AA'),
                help="Your main brand color (HEX)"
            )

            st.markdown(f"""
                <div style='padding: 10px; background: {primary_color}; color: white;
                     border-radius: 5px; text-align: center; margin-top: 10px;'>
                    <strong>Selected Color</strong><br>
                    {primary_color.upper()}
                </div>
            """, unsafe_allow_html=True)

        # Show complementary colors
        if primary_color:
            colors = generate_complementary_colors(primary_color)
            st.markdown("**Auto-Generated Complementary Colors:**")

            color_cols = st.columns(4)
            with color_cols[0]:
                st.markdown(f"""
                    <div style='padding: 20px; background: {colors["primary"]};
                         border-radius: 5px; text-align: center;'>
                        <small style='color: {colors["text"]}'>Primary</small><br>
                        <strong style='color: {colors["text"]}'>{colors["primary"]}</strong>
                    </div>
                """, unsafe_allow_html=True)

            with color_cols[1]:
                st.markdown(f"""
                    <div style='padding: 20px; background: {colors["accent"]};
                         border-radius: 5px; text-align: center;'>
                        <small style='color: {colors["text"]}'>Accent</small><br>
                        <strong style='color: {colors["text"]}'>{colors["accent"]}</strong>
                    </div>
                """, unsafe_allow_html=True)

            with color_cols[2]:
                st.markdown(f"""
                    <div style='padding: 20px; background: {colors["text"]};
                         border-radius: 5px; text-align: center;'>
                        <small style='color: white' if colors["text"] == "#1A1A1A" else 'color: black'>Text</small><br>
                        <strong style='color: white' if colors["text"] == "#1A1A1A" else 'color: black'>{colors["text"]}</strong>
                    </div>
                """, unsafe_allow_html=True)

            with color_cols[3]:
                st.markdown(f"""
                    <div style='padding: 20px; background: {colors["secondary_text"]};
                         border-radius: 5px; text-align: center;'>
                        <small>Secondary</small><br>
                        <strong>{colors["secondary_text"]}</strong>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # SECTION 3: Company Profile
        st.markdown("### 📝 3. Company Profile")
        st.caption('This text will be used to populate the "About Us" section of your RFPs.')

        company_boilerplate = st.text_area(
            "Company Boilerplate* (Max 300 words)",
            placeholder="Paste your standard 'Who We Are' elevator pitch here. Include your mission and key capabilities.\n\nExample:\n\nAcme Corporation is a leading provider of innovative solutions in the technology sector. Founded in 2010, we specialize in delivering cutting-edge software and consulting services to enterprise clients worldwide. Our mission is to empower businesses through digital transformation...",
            height=150,
            max_chars=2000,
            help="Your standard company description",
            value=st.session_state.brand_data.get('company_boilerplate', '')
        )

        word_count = len(company_boilerplate.split())
        st.caption(f"Words: {word_count}/300")

        st.markdown("---")

        # SECTION 4: Legal Footer
        st.markdown("### ⚖️ 4. Legal Footer")
        st.caption("Appears at the bottom of every page.")

        default_confidentiality = f"Confidential & Proprietary. Copyright © {datetime.now().year} [Company Name]. All rights reserved."

        use_default_footer = st.checkbox(
            "Use default confidentiality statement",
            value=st.session_state.brand_data.get('use_default_footer', True)
        )

        if use_default_footer:
            confidentiality_statement = default_confidentiality
            st.info(f"**Default Statement:** {default_confidentiality}")
        else:
            confidentiality_statement = st.text_area(
                "Custom Confidentiality Statement",
                placeholder="Enter your custom confidentiality statement...",
                height=80,
                value=st.session_state.brand_data.get('confidentiality_statement', '')
            )

        st.markdown("---")

        # Additional Settings
        with st.expander("⚙️ Additional Settings (Optional)"):
            col1, col2 = st.columns(2)

            with col1:
                industry = st.selectbox(
                    "Industry",
                    ["Technology", "Consulting", "Manufacturing", "Healthcare",
                     "Finance", "Education", "Government", "Other"],
                    index=0
                )

                company_size = st.selectbox(
                    "Company Size",
                    ["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"],
                    index=2
                )

            with col2:
                timezone = st.selectbox(
                    "Timezone",
                    ["UTC", "EST", "PST", "CST", "GMT", "CET", "AST", "GST"],
                    index=7
                )

                currency = st.selectbox(
                    "Default Currency",
                    ["USD", "EUR", "GBP", "AED", "SAR", "QAR", "KWD"],
                    index=3
                )

        # Submit button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            submitted = st.form_submit_button(
                "✅ Complete Brand Setup",
                use_container_width=True,
                type="primary"
            )

        # Form validation and submission
        if submitted:
            errors = []

            # Validate required fields
            if not company_name or len(company_name.strip()) < 2:
                errors.append("Company Name is required (minimum 2 characters)")

            if not hq_address or len(hq_address.strip()) < 10:
                errors.append("Headquarters Address is required (minimum 10 characters)")

            if not website_url or not validate_url(website_url):
                errors.append("Valid Website URL is required (must start with http:// or https://)")

            if not contact_email or not validate_email(contact_email):
                errors.append("Valid Proposal Contact Email is required")

            if logo_file is None:
                errors.append("Company Logo is required")

            if not validate_hex_color(primary_color):
                errors.append("Valid Primary Brand Color is required")

            if not company_boilerplate or len(company_boilerplate.strip()) < 50:
                errors.append("Company Boilerplate is required (minimum 50 characters)")

            if word_count > 300:
                errors.append("Company Boilerplate must be 300 words or less")

            # Display errors or save data
            if errors:
                st.error("**Please fix the following errors:**\n\n" + "\n".join([f"• {error}" for error in errors]))
            else:
                # Save company data
                with st.spinner("🔄 Setting up your brand..."):
                    # Generate color palette
                    color_palette = generate_complementary_colors(primary_color)

                    # Prepare company data
                    company_data = {
                        'company_name': company_name.strip(),
                        'hq_address': hq_address.strip(),
                        'website_url': website_url.strip(),
                        'contact_email': contact_email.strip(),
                        'phone': phone.strip() if phone else None,
                        'company_boilerplate': company_boilerplate.strip(),
                        'confidentiality_statement': confidentiality_statement,
                        'use_default_footer': use_default_footer,
                        'brand_colors': color_palette,
                        'industry': industry,
                        'company_size': company_size,
                        'timezone': timezone,
                        'currency': currency,
                        'onboarding_completed': True
                    }

                    # Create company
                    company_id = db.create_company(company_data)

                    # Save logo
                    if logo_file is not None:
                        logo_path = db.save_logo(company_id, logo_file.read(), logo_file.name)
                        db.update_company(company_id, {'logo_path': logo_path})

                    # Link company to user
                    if st.session_state.get('user'):
                        user_id = st.session_state.user.get('id')
                        if user_id:
                            db.update_user(user_id, {'company_id': company_id})
                            st.session_state.user['company_id'] = company_id

                    # Store in session
                    st.session_state.company_id = company_id
                    st.session_state.company = company_data
                    st.session_state.onboarding_completed = True

                    st.success("✅ **Brand setup completed successfully!**")
                    st.balloons()

                    # Show summary
                    st.markdown("---")
                    st.markdown("### 📊 Setup Summary")

                    summary_col1, summary_col2 = st.columns(2)

                    with summary_col1:
                        st.markdown(f"""
                        **Company Information:**
                        - **Name:** {company_name}
                        - **Email:** {contact_email}
                        - **Website:** {website_url}
                        - **Industry:** {industry}
                        """)

                    with summary_col2:
                        st.markdown(f"""
                        **Brand Colors:**
                        - **Primary:** {color_palette['primary']}
                        - **Accent:** {color_palette['accent']}
                        - **Text:** {color_palette['text']}
                        """)

                    st.info("🎉 Your brand is now configured! You can proceed to create your first proposal.")

                    # Redirect button
                    if st.button("📊 Go to Dashboard", type="primary", use_container_width=True):
                        st.switch_page("pages/dashboard.py")


if __name__ == "__main__":
    main()
