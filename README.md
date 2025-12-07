# ⚡ BidForge AI

**Premium Construction Bidding Automation System for GCC Markets**

A world-class Streamlit application that revolutionizes construction bidding with AI-powered proposal generation, risk assessment, and intelligent document analysis. Designed with GCC clientele aesthetics in mind featuring a premium Deep Teal (#0d7377) and Antique Gold (#b8995a) color palette.

![Version](https://img.shields.io/badge/version-1.0.0-0d7377)
![Python](https://img.shields.io/badge/python-3.11+-b8995a)
![Streamlit](https://img.shields.io/badge/streamlit-1.40+-0d7377)
![License](https://img.shields.io/badge/license-MIT-b8995a)

---

## ✨ Features

### 🤖 **Multi-AI Bid Generation**
- Support for **OpenAI GPT-4o**, **Claude Sonnet 4.5**, **Google Gemini 2.0**, and **DeepSeek**
- Side-by-side model comparison for optimal proposal quality
- Iterative refinement through AI-powered chat interface
- Context-aware generation using RAG (Retrieval-Augmented Generation)

### 📊 **Intelligent RFP Analysis**
- Automated risk scoring (Quality, Clarity, Doability, Vendor Risk)
- Red flag detection with severity classification
- Opportunity identification for competitive advantage
- Actionable recommendations with time estimates and ownership

### 🔍 **Advanced Conflict Detection**
- Semantic conflict detection using embeddings
- Numeric value discrepancy identification
- Cross-document consistency checking
- Severity-based prioritization

### 🎯 **ML Win Probability Prediction**
- 8-factor feature analysis
- Statistical scoring model with confidence metrics
- Risk and strength factor identification
- Optimization recommendations with projected impact

### 📱 **WhatsApp Integration**
- Request missing documents via WhatsApp Business API
- Automated professional message generation
- Email fallback for flexible communication

### 🎨 **Premium GCC-Inspired Design**
- Deep Teal (#0d7377) and Antique Gold (#b8995a) color scheme
- Three-font hierarchy: Syne (headlines), Inter (body), Fraunces (accents)
- Sophisticated hover effects and animations
- Mobile-responsive design

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager
- API keys for AI providers (OpenAI, Anthropic, etc.)

### Installation

1. **Clone the repository**
   ```bash
   cd BidForgeAI
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```bash
   OPENAI_API_KEY=sk-your-openai-key
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
   GOOGLE_API_KEY=AIza-your-google-key
   # ... other configuration
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the application**

   Open your browser and navigate to: `http://localhost:8501`

---

## 🔐 Demo Login Credentials

Access the application using these demo accounts:

| Role | Email | Password |
|------|-------|----------|
| **Administrator** | admin@bidforge.ai | Admin@123 |
| **Project Manager** | manager@bidforge.ai | Manager@123 |
| **Regular User** | user@bidforge.ai | User@123 |

---

## 📁 Project Structure

```
BidForgeAI/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # This file
│
├── pages/                          # Application pages
│   ├── __init__.py
│   ├── login.py                   # Authentication page
│   ├── dashboard.py               # Main dashboard
│   ├── project_workspace.py       # Project management
│   ├── rfp_analysis.py            # RFP analysis & risk assessment
│   ├── bid_generation.py          # AI bid generation
│   ├── conflict_detection.py      # Document conflict detection
│   ├── win_probability.py         # Win probability ML prediction
│   └── settings.py                # Application settings
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── theme.py                   # GCC-inspired theme & styling
│   ├── auth.py                    # Authentication utilities
│   ├── ai_services.py             # AI provider integrations
│   ├── database.py                # Database operations
│   └── document_processor.py      # Document text extraction
│
└── data/                           # Data storage (auto-created)
    ├── projects/
    ├── documents/
    ├── analyses/
    ├── bids/
    ├── conflicts/
    └── predictions/
```

---

## 🎨 Design System

### Color Palette (GCC-Inspired)

```css
--deep-teal:         #0d7377  /* Primary brand color */
--deep-teal-dark:    #0a5a5d  /* Hover states */
--deep-teal-light:   #14a0a6  /* Accents */
--antique-gold:      #b8995a  /* Secondary color */
--antique-gold-light:#d4b676  /* Highlights */
--charcoal:          #1a1a1a  /* Background */
```

### Typography

- **Headlines**: Syne (700-800 weight)
- **Body Text**: Inter (400-600 weight)
- **Accents**: Fraunces (600-700 weight)

---

## 🔧 Configuration

### API Configuration

Configure AI providers in the Settings page or via environment variables. See `.env.example` for all options.

---

## 📖 User Guide

### Creating a New Project

1. Navigate to **Projects** → **New Project** tab
2. Fill in project details (name, client, deadline)
3. Upload RFQ documents (PDF, DOCX, XLSX, MSG, ZIP)
4. Enable auto-analysis option (recommended)
5. Click **Create Project**

### Running RFP Analysis

1. Go to **RFP Analysis** page
2. Select your project
3. Click **Run Analysis**
4. Review scores, findings, and recommendations

### Generating a Bid

1. Navigate to **Bid Generation**
2. Select project and AI model(s)
3. Adjust generation settings
4. Click **Generate Bid Proposal**
5. Refine using chat interface
6. Export to HTML or PDF

---

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect repository and add environment variables
4. Deploy!

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

**Built with ❤️ for the GCC Construction Industry**

</div>
