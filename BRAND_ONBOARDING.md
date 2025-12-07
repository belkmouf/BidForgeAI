# 🚀 Brand Setup Onboarding Feature

## Overview

This feature implements a comprehensive brand setup onboarding process for new users/companies during account creation in BidForge AI. It allows companies to configure their essential proposal branding in approximately 5 minutes.

## Features Implemented

### 1. **User Registration System** (`pages/register.py`)
- New user account creation
- Email validation
- Strong password requirements:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one number
  - At least one special character
- Password confirmation
- Terms and conditions acceptance
- Automatic redirect to brand setup after registration

### 2. **Brand Onboarding Page** (`pages/brand_onboarding.py`)

#### Section 1: Company Basics
Required for legal validity on cover pages and footers:
- **Company Name*** - As it should appear on contracts
- **Headquarters Address*** - Full physical address
- **Website URL*** - Company website
- **Proposal Contact Email*** - Where replies should be sent
- **Contact Phone Number** - Optional

#### Section 2: Visual Identity
Assets used to auto-theme the entire document:
- **Company Logo*** - Upload PNG or SVG (transparent background recommended)
  - Live preview of uploaded logo
  - Saved to `data/uploads/logos/` directory
- **Primary Brand Color*** - HEX color picker
  - Auto-generates complementary colors:
    - Accent color
    - Text color
    - Secondary text color
  - Visual preview of all generated colors

#### Section 3: Company Profile
- **Company Boilerplate*** - Max 300 words
  - Used to populate "About Us" section in RFPs
  - Word counter included
  - Standard elevator pitch with mission and capabilities

#### Section 4: Legal Footer
- **Confidentiality Statement** - Optional
  - Default: "Confidential & Proprietary. Copyright © [Year] [Company Name]"
  - Custom statement option

#### Additional Settings (Optional)
- Industry selection
- Company size
- Timezone
- Default currency

### 3. **Database Schema** (`utils/database.py`)

#### New Database Methods:

**Company Management:**
- `create_company(company_data)` - Create new company with brand settings
- `get_company(company_id)` - Retrieve company by ID
- `update_company(company_id, updates)` - Update company data
- `list_companies()` - List all companies

**User Management:**
- `create_user(user_data)` - Create new user account
- `get_user(user_id)` - Get user by ID
- `get_user_by_email(email)` - Find user by email
- `update_user(user_id, updates)` - Update user data
- `list_users(company_id)` - List users by company

**File Upload:**
- `save_logo(company_id, logo_data, filename)` - Save company logo
- `get_logo_path(company_id)` - Retrieve logo path

#### Data Structure:

**Company Object:**
```json
{
  "id": "COMP-20241207-120000",
  "company_name": "Acme Corporation",
  "hq_address": "123 Business Street...",
  "website_url": "https://acme.com",
  "contact_email": "proposals@acme.com",
  "phone": "+1 555-123-4567",
  "company_boilerplate": "Company description...",
  "confidentiality_statement": "Confidential & Proprietary...",
  "use_default_footer": true,
  "brand_colors": {
    "primary": "#0055AA",
    "accent": "#0066CC",
    "text": "#FFFFFF",
    "secondary_text": "#E0E0E0"
  },
  "industry": "Technology",
  "company_size": "51-200",
  "timezone": "GST",
  "currency": "AED",
  "logo_path": "data/uploads/logos/COMP-20241207-120000.png",
  "onboarding_completed": true,
  "created_at": "2024-12-07T12:00:00",
  "updated_at": "2024-12-07T12:00:00"
}
```

**User Object:**
```json
{
  "id": "USR-20241207-120000",
  "name": "John Smith",
  "email": "john@acme.com",
  "password": "$2b$12$hashed_password",
  "role": "Admin",
  "company_id": "COMP-20241207-120000",
  "created_at": "2024-12-07T12:00:00",
  "updated_at": "2024-12-07T12:00:00"
}
```

### 4. **Authentication Updates** (`utils/auth.py`)

**New Functions:**
- `register_user(name, email, password, role)` - Register new user
  - Checks for existing email
  - Hashes password with bcrypt
  - Creates user record
  - Returns user_id or None

**Updated Functions:**
- `login_user(email, password)` - Enhanced authentication
  - Checks database users first
  - Falls back to demo users for backward compatibility
  - Loads company data if available
  - Sets `onboarding_completed` flag in session

- `logout_user()` - Enhanced logout
  - Clears company and onboarding state

### 5. **Login Page Updates** (`pages/login.py`)

**New Features:**
- "Create New Account" button linking to registration
- Automatic redirect to brand onboarding if not completed
- Maintains demo login functionality for testing

## User Flow

### Registration & Onboarding Flow:

```
1. User visits Login Page
   ↓
2. Clicks "Create New Account"
   ↓
3. Fills Registration Form
   - Full Name
   - Email
   - Password (with strength validation)
   - Confirms Password
   - Accepts Terms
   ↓
4. Account Created → Auto-redirect to Brand Onboarding
   ↓
5. Completes Brand Setup Form
   - Company Basics
   - Visual Identity (Logo + Colors)
   - Company Profile
   - Legal Footer
   - Additional Settings
   ↓
6. Brand Setup Complete → Redirect to Dashboard
   ↓
7. Company data saved and linked to user
```

### Login Flow for Existing Users:

```
1. User enters credentials
   ↓
2. System authenticates
   ↓
3. Check if onboarding completed
   ↓
4a. If NO → Redirect to Brand Onboarding
4b. If YES → Go to Dashboard
```

## Validation Rules

### Registration:
- Full name: Minimum 2 characters
- Email: Valid email format
- Password: Strong password (uppercase, lowercase, number, special char, 8+ chars)
- Passwords must match
- Terms must be accepted

### Brand Onboarding:
- Company Name: Minimum 2 characters
- HQ Address: Minimum 10 characters
- Website URL: Must start with http:// or https://
- Contact Email: Valid email format
- Logo: Required (PNG, SVG, JPG, JPEG)
- Primary Color: Valid HEX format (#RRGGBB)
- Company Boilerplate: Minimum 50 characters, maximum 300 words

## File Structure

```
/home/user/BidForgeAI/
├── pages/
│   ├── login.py                    # Updated with registration link
│   ├── register.py                 # NEW - User registration page
│   └── brand_onboarding.py         # NEW - Brand setup wizard
├── utils/
│   ├── auth.py                     # Updated with registration
│   └── database.py                 # Extended with company/user management
├── data/                           # File-based storage
│   ├── companies/                  # Company JSON files
│   ├── users/                      # User JSON files
│   └── uploads/
│       └── logos/                  # Company logos
└── BRAND_ONBOARDING.md            # This documentation
```

## Session State Variables

After successful onboarding, the following are set in `st.session_state`:

```python
{
    'authenticated': True,
    'user': {
        'id': 'USR-xxx',
        'name': 'John Smith',
        'email': 'john@acme.com',
        'role': 'Admin',
        'company_id': 'COMP-xxx'
    },
    'company': {
        # Full company object with brand settings
    },
    'company_id': 'COMP-xxx',
    'onboarding_completed': True,
    'token': 'jwt_token_here'
}
```

## Demo Accounts

Demo accounts skip onboarding and work as before:
- **Admin:** admin@bidforge.ai / Admin@123
- **Manager:** manager@bidforge.ai / Manager@123
- **User:** user@bidforge.ai / User@123

## Color Auto-Generation Algorithm

The system automatically generates complementary colors based on the primary brand color:

1. **Primary Color** - User-selected HEX color
2. **Accent Color** - Calculated as:
   - If brightness < 128: Lighter version (multiply RGB by 1.2)
   - If brightness ≥ 128: Darker version (multiply RGB by 0.8)
3. **Text Color** - Based on background brightness:
   - Dark background (< 128): White text (#FFFFFF)
   - Light background (≥ 128): Dark text (#1A1A1A)
4. **Secondary Text** - Muted version for less emphasis

## Future Enhancements

Potential improvements for future iterations:

1. **PostgreSQL Migration** - Move from file-based to PostgreSQL database
2. **Multi-user Support** - Team member invitations and role management
3. **Logo Requirements** - Enforce transparent background validation
4. **Brand Preview** - Show live preview of proposal with brand settings
5. **Export/Import** - Export brand settings, import from existing templates
6. **Theme Customization** - More granular control over colors and styles
7. **Email Verification** - Verify email addresses during registration
8. **Password Reset** - Forgot password functionality
9. **Company Settings** - Allow editing brand settings after onboarding
10. **Multi-language** - Support for Arabic and French interfaces

## Testing

To test the complete onboarding flow:

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Create a new account:**
   - Click "Create New Account" on login page
   - Fill in registration form
   - Submit to create account

3. **Complete brand setup:**
   - Upload company logo
   - Select primary brand color
   - Fill in company details
   - Submit brand setup

4. **Verify:**
   - Check `data/companies/` for company JSON
   - Check `data/users/` for user JSON
   - Check `data/uploads/logos/` for uploaded logo
   - Login again and verify no onboarding redirect

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens for session management
- Email validation to prevent invalid formats
- File upload restricted to image formats
- No SQL injection (using file-based storage)
- Session state properly cleared on logout

## Support

For issues or questions about the brand onboarding feature, please refer to the main BidForge AI documentation or contact the development team.

---

**Version:** 1.0.0
**Last Updated:** December 7, 2024
**Author:** BidForge AI Development Team
