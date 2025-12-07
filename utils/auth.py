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
    In production, this would query the database
    """
    # For demo purposes, using hardcoded users
    # In production, query from database
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

    user = demo_users.get(email)
    if user and verify_password(password, user['password']):
        st.session_state.authenticated = True
        st.session_state.user = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role']
        }
        st.session_state.token = create_token(st.session_state.user)
        return True

    return False


def logout_user():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.token = None


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
