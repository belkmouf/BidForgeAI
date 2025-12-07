"""
Authentication and session management for BidForge AI
"""

import streamlit as st
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
import os


JWT_SECRET = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-this")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def create_token(user_data: Dict) -> str:
    """Create a JWT token"""
    payload = {
        'user_id': user_data.get('id'),
        'email': user_data.get('email'),
        'role': user_data.get('role'),
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[Dict]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def check_authentication() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)


def login_user(email: str, password: str) -> bool:
    """
    Authenticate user credentials
    Checks both database users and demo users
    """
    from utils.database import db

    # First, try to find user in database
    user = db.get_user_by_email(email)

    if user and verify_password(password, user.get('password', '')):
        st.session_state.authenticated = True
        st.session_state.user = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user.get('role', 'User'),
            'company_id': user.get('company_id')
        }
        st.session_state.token = create_token(st.session_state.user)

        # Check if company onboarding is completed
        if user.get('company_id'):
            company = db.get_company(user['company_id'])
            if company:
                st.session_state.company = company
                st.session_state.onboarding_completed = company.get('onboarding_completed', False)

        return True

    # Fallback to demo users for backward compatibility
    demo_users = {
        'admin@bidforge.ai': {
            'id': '1',
            'name': 'Ahmed Al-Mansouri',
            'email': 'admin@bidforge.ai',
            'password': hash_password('Admin@123'),
            'role': 'Admin'
        },
        'manager@bidforge.ai': {
            'id': '2',
            'name': 'Fatima Al-Sayed',
            'email': 'manager@bidforge.ai',
            'password': hash_password('Manager@123'),
            'role': 'Manager'
        },
        'user@bidforge.ai': {
            'id': '3',
            'name': 'Mohammed Al-Rashid',
            'email': 'user@bidforge.ai',
            'password': hash_password('User@123'),
            'role': 'User'
        }
    }

    demo_user = demo_users.get(email)
    if demo_user and verify_password(password, demo_user['password']):
        st.session_state.authenticated = True
        st.session_state.user = {
            'id': demo_user['id'],
            'name': demo_user['name'],
            'email': demo_user['email'],
            'role': demo_user['role']
        }
        st.session_state.token = create_token(st.session_state.user)
        st.session_state.onboarding_completed = True  # Demo users skip onboarding
        return True

    return False


def register_user(name: str, email: str, password: str, role: str = 'Admin') -> Optional[str]:
    """
    Register a new user account
    Returns user_id on success, None on failure
    """
    from utils.database import db

    # Check if user already exists
    existing_user = db.get_user_by_email(email)
    if existing_user:
        return None

    # Create user
    user_data = {
        'name': name,
        'email': email,
        'password': hash_password(password),
        'role': role,
        'company_id': None  # Will be set after company onboarding
    }

    user_id = db.create_user(user_data)
    return user_id


def logout_user():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.token = None
    st.session_state.company = None
    st.session_state.onboarding_completed = False


def require_permission(permission: str) -> bool:
    """Check if current user has required permission"""
    if not check_authentication():
        return False

    role = st.session_state.user.get('role', '')

    # Admin has all permissions
    if role == 'Admin':
        return True

    # Define role permissions
    role_permissions = {
        'Manager': [
            'view_projects', 'create_project', 'edit_project',
            'view_analysis', 'generate_bid', 'view_conflicts',
            'view_win_probability'
        ],
        'User': [
            'view_projects', 'create_project', 'edit_project',
            'view_analysis', 'generate_bid'
        ],
        'Viewer': ['view_projects', 'view_analysis']
    }

    return permission in role_permissions.get(role, [])
