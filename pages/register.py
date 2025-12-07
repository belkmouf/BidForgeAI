"""
Registration page for BidForge AI
User and company account creation
"""

import streamlit as st
import re
from utils.auth import register_user
from utils.theme import apply_theme


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength and return (is_valid, message)"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    return True, "Strong password"


def main():
    # Apply theme
    apply_theme()

    # Header
    st.markdown("""
        <h1 style='text-align: center; color: #C5A572; margin-bottom: 10px;'>
            Create Your Account
        </h1>
        <p style='text-align: center; color: #666; margin-bottom: 40px;'>
            Join BidForge AI and start creating winning proposals
        </p>
    """, unsafe_allow_html=True)

    # Registration form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("registration_form"):
            st.markdown("### 👤 Account Information")

            full_name = st.text_input(
                "Full Name*",
                placeholder="e.g., John Smith",
                help="Your full name as it should appear in the system"
            )

            email = st.text_input(
                "Email Address*",
                placeholder="your.email@company.com",
                help="This will be your username for login"
            )

            col_pass1, col_pass2 = st.columns(2)

            with col_pass1:
                password = st.text_input(
                    "Password*",
                    type="password",
                    help="Minimum 8 characters with uppercase, lowercase, number, and special character"
                )

            with col_pass2:
                confirm_password = st.text_input(
                    "Confirm Password*",
                    type="password"
                )

            # Password strength indicator
            if password:
                is_valid, message = validate_password_strength(password)
                if is_valid:
                    st.success(f"✅ {message}")
                else:
                    st.warning(f"⚠️ {message}")

            st.markdown("---")

            # Terms and conditions
            agree_terms = st.checkbox(
                "I agree to the Terms of Service and Privacy Policy",
                value=False
            )

            # Submit button
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                "🚀 Create Account & Setup Brand",
                use_container_width=True,
                type="primary"
            )

        # Form validation
        if submitted:
            errors = []

            # Validate full name
            if not full_name or len(full_name.strip()) < 2:
                errors.append("Full Name is required (minimum 2 characters)")

            # Validate email
            if not email or not validate_email(email):
                errors.append("Valid Email Address is required")

            # Validate password
            is_valid_password, password_message = validate_password_strength(password)
            if not is_valid_password:
                errors.append(password_message)

            # Validate password match
            if password != confirm_password:
                errors.append("Passwords do not match")

            # Validate terms
            if not agree_terms:
                errors.append("You must agree to the Terms of Service and Privacy Policy")

            # Display errors or register user
            if errors:
                st.error("**Please fix the following errors:**\n\n" + "\n".join([f"• {error}" for error in errors]))
            else:
                with st.spinner("🔄 Creating your account..."):
                    # Register user
                    user_id = register_user(
                        name=full_name.strip(),
                        email=email.strip().lower(),
                        password=password,
                        role='Admin'  # First user is admin of their company
                    )

                    if user_id:
                        # Set session state
                        st.session_state.user_id = user_id
                        st.session_state.user_email = email.strip().lower()
                        st.session_state.user_name = full_name.strip()
                        st.session_state.authenticated = True
                        st.session_state.user = {
                            'id': user_id,
                            'name': full_name.strip(),
                            'email': email.strip().lower(),
                            'role': 'Admin'
                        }
                        st.session_state.onboarding_completed = False

                        st.success("✅ **Account created successfully!**")
                        st.info("🎨 **Next Step:** Complete your brand setup to start creating proposals")

                        # Add redirect button
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("➡️ Continue to Brand Setup", type="primary", use_container_width=True):
                            st.switch_page("pages/brand_onboarding.py")

                        # Auto-redirect after 3 seconds
                        st.markdown("""
                            <script>
                            setTimeout(function() {
                                window.location.href = '/brand_onboarding';
                            }, 3000);
                            </script>
                        """, unsafe_allow_html=True)

                    else:
                        st.error("❌ **Registration failed:** An account with this email already exists. Please use a different email or try logging in.")

        # Login link
        st.markdown("---")
        st.markdown("""
            <p style='text-align: center; color: #666;'>
                Already have an account? <a href='/login' style='color: #C5A572; text-decoration: none;'>Login here</a>
            </p>
        """, unsafe_allow_html=True)

        if st.button("← Back to Login", use_container_width=True):
            st.switch_page("pages/login.py")


if __name__ == "__main__":
    main()
