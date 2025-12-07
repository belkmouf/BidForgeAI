# BidForge AI - Construction Bidding Automation System

## Overview

BidForge AI is a construction bidding automation system that streamlines the proposal generation process for construction companies. The application ingests RFQ documents (PDFs, emails, ZIP files), uses Retrieval-Augmented Generation (RAG) with vector search to find relevant context from current and historical "Closed-Won" projects, and generates professional HTML bid responses using AI. Users can iteratively refine bids through an AI-powered chat interface.

The system is designed as a full-stack web application with a React frontend and Express/Node.js backend, leveraging PostgreSQL with pgvector for semantic search capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework & Build System**
- React 18 with TypeScript using Vite as the build tool
- Wouter for lightweight client-side routing
- TanStack Query (React Query) for server state management and API data fetching
- Single-page application (SPA) architecture with client-side routing

**UI Component System**
- Shadcn UI component library (New York style variant) with Radix UI primitives
- Tailwind CSS v4 for styling with custom design tokens
- Lucide React for iconography
- GSAP for scroll-based and entrance animations

**Version 2 Design System (Somerstone-Inspired)**
- Gulf Executive color palette: Charcoal (#1a1a1a), Deep Teal (#0d7377), Antique Gold (#b8995a)
- Three-font hierarchy: Syne (display/headlines), Inter (body text), Fraunces (accents)
- Premium styling with refined spacing, card hover effects, and sophisticated color usage
- Landing page at "/" with Hero, Features, Testimonials, CTA sections
- Dashboard moved to "/dashboard" route

**Rich Text Editing**
- Tiptap editor for WYSIWYG bid document editing
- Support for tables, headings, lists, and rich formatting
- Extensions for placeholder text and table functionality

**Key Frontend Features**
- Dashboard with project pipeline visualization using Recharts
- Project workspace with drag-and-drop file upload
- Resizable panel layout for split-screen editing
- AI generation panel with model selection (OpenAI, Anthropic, Gemini)
- Iterative refinement through chat interface

### Backend Architecture

**Server Framework**
- Express.js with TypeScript running on Node.js
- HTTP server with middleware for JSON parsing and URL encoding
- Custom request logging with timestamp formatting
- Development mode with Vite middleware for HMR
- Production mode serving static built assets

**API Design**
- RESTful API endpoints under `/api` prefix
- Multipart form data handling with Multer for file uploads (50MB limit)
- Zod schema validation for request payloads
- Error handling with structured JSON responses

**Database Layer**
- Drizzle ORM for type-safe database queries
- Neon serverless PostgreSQL with WebSocket support
- Schema-first design with TypeScript type generation
- Migration management via Drizzle Kit

**AI Integration Strategy**
- Multiple AI provider support: OpenAI (GPT-4o), Anthropic (Claude Sonnet 4.5), Google Gemini (2.5 Flash), DeepSeek
- Separate service modules for each AI provider
- Unified interface for bid generation and refinement
- User-selectable model at runtime
- Multi-model comparison: Request multiple AI providers in parallel for side-by-side draft comparison
- API accepts `models: ['openai', 'anthropic', 'gemini', 'deepseek']` array for parallel generation

**RAG Implementation**
- Vector embeddings using OpenAI's text-embedding-3-small model (1536 dimensions)
- pgvector extension for similarity search
- Document chunking strategy for efficient retrieval
- Context aggregation from current project documents and historical winning bids

### Data Storage Solutions

**Database Schema**

1. **Projects Table**
   - UUID primary key with auto-generation
   - Status tracking: Active, Submitted, Closed-Won, Closed-Lost
   - JSONB metadata field for flexible attributes
   - Client name and project name fields

2. **Documents Table**
   - Auto-incrementing integer ID
   - Foreign key reference to projects with cascade delete
   - Text content storage and processing status flag
   - Upload timestamp tracking

3. **Document Chunks Table**
   - Auto-incrementing integer ID
   - Foreign key reference to documents with cascade delete
   - Text content with vector embeddings (1536 dimensions)
   - Chunk index for ordering

**Storage Layer Abstraction**
- Interface-based design (`IStorage`) for testability
- `DatabaseStorage` implementation using Drizzle ORM
- Methods for CRUD operations on projects, documents, and chunks
- Similarity search using cosine distance with pgvector
- Dashboard statistics aggregation (pipeline counts, win rate)

### RFP Analysis & Risk Assessment Module

**Analysis Features**
- AI-powered RFP document analysis using OpenAI GPT-4o
- Four key scores: Quality (0-100), Clarity (0-100), Doability (0-100), Vendor Risk (0-100)
- Overall risk level assessment: Low, Medium, High, Critical
- Vendor payment history tracking from internal database
- Missing documents detection with request functionality
- Red flags and opportunities identification
- Actionable recommendations with priority and time estimates

**Missing Documents Request Feature**
- WhatsApp and Email buttons to request missing documents from vendors
- AI-generated professional messages tailored for each channel
- Editable message preview before sending
- WhatsApp messages sent directly via Meta Business API
- Email opens in user's default email client with pre-filled content

**Database Tables**
- `rfp_analyses` - Stores analysis results with scores and findings
- `analysis_alerts` - Tracks actionable alerts with resolution status
- `vendor_database` - Payment history and ratings for known vendors

### WhatsApp Integration

**Meta WhatsApp Business API**
- Official WhatsApp Node.js SDK for Cloud API
- Send text messages, documents, and template messages
- Receive messages via webhook with signature verification
- Configuration page at `/whatsapp` route
- Missing documents request integration from Analysis module

**Required Environment Variables:**
- `WA_PHONE_NUMBER_ID` - Phone number ID from Meta Developer Console
- `CLOUD_API_ACCESS_TOKEN` - API access token
- `WEBHOOK_VERIFY_TOKEN` - Token for webhook verification (default: bidforge_webhook_token)
- `WA_APP_SECRET` - App secret for webhook signature verification

### Authentication and Authorization

**JWT-Based Authentication**
- Secure user registration and login with bcrypt password hashing
- JWT access tokens (24h expiry) and refresh tokens (7d expiry)
- Password validation requirements (8+ chars, uppercase, lowercase, number)
- Token-based API authentication via Authorization header

**Database Tables**
- `users` - User accounts with email, password hash, name, role, timestamps
- `sessions` - Refresh token storage with expiration tracking
- `roles` - Role definitions with permission arrays (RBAC)
- `user_roles` - Junction table for user-role assignments (supports project-specific roles)

**Role-Based Access Control (RBAC)**
- Four user roles: Admin, Manager, User, Viewer
- Permission-based middleware for route protection
- Granular permissions for projects, documents, analysis, generation, and user management
- Admin role has full system access

**Security Features**
- Helmet.js for security headers
- Rate limiting: 1000 requests/15min (API), 20 requests/15min (auth)
- CORS with configurable allowed origins
- Request body size limits (10MB)

**Frontend Authentication**
- Login and Register pages at `/login` and `/register`
- Zustand store for auth state management with localStorage persistence
- Protected routes redirecting to login when not authenticated
- User profile management in Settings page with password change

**API Endpoints**
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user
- `PATCH /api/auth/profile` - Update user profile
- `POST /api/auth/change-password` - Change password
- `POST /api/auth/logout` - Logout (client-side token removal)

### AI Agent System (LangChain/LangGraph)

**Agent Orchestration Framework**
- LangChain ecosystem for AI agent development
- LangGraph StateGraph for workflow orchestration
- Multi-agent pipeline: Intake → Analysis → Decision → Generation → Review
- Conditional routing based on analysis results (risk/doability thresholds)

**Agent Architecture**
- `BaseAgent` abstract class with execution wrapping and logging
- `AgentRegistry` for agent registration and lookup
- `BidWorkflowAnnotation` for typed state management with reducers
- Zod schemas for all agent inputs/outputs

**Individual Agents**
1. **IntakeAgent** - Loads and validates project documents from database
2. **AnalysisAgent** - AI-powered RFQ analysis with scoring (quality, clarity, doability, vendor risk)
3. **DecisionAgent** - Strategic bid approach decisions (aggressive/balanced/conservative)
4. **GenerationAgent** - Professional HTML bid proposal generation
5. **ReviewAgent** - Quality assessment with pass/fail and retry logic

**Workflow Features**
- Automatic retry on review failure (max 3 attempts)
- Risk-based early termination (Critical risk or low doability)
- Streaming support for real-time progress updates
- Configurable thresholds via OrchestratorConfig

**Files**
- `server/agents/base-agent.ts` - Abstract agent class and registry
- `server/agents/state.ts` - Workflow state schemas and annotations
- `server/agents/orchestrator.ts` - LangGraph StateGraph configuration
- `server/agents/index.ts` - Agent exports and initialization

### Conflict Detection System

**Semantic Conflict Detection**
- AI-powered detection of contradictory statements in bid documents
- Uses OpenAI embeddings for semantic similarity analysis
- Cosine similarity threshold of 0.85 for conflict identification
- Lazy initialization to avoid API key errors at startup

**Numeric Conflict Detection**
- Regex-based extraction of numbers, dates, percentages, and currencies
- Context-aware grouping of values for conflict detection
- 1% threshold for numeric value conflicts
- Severity scoring based on conflict magnitude

**Database Tables**
- `document_conflicts` - Stores detected conflicts with source/target locations
- `conflict_detection_runs` - Tracks detection run history with statistics

**API Endpoints**
- `POST /api/conflicts/detect/:projectId` - Run conflict detection
- `GET /api/conflicts/:projectId` - Get conflicts with filtering
- `GET /api/conflicts/:projectId/stats` - Get conflict statistics
- `PATCH /api/conflicts/:conflictId/status` - Update conflict status

**Frontend Components**
- `ConflictDetection.tsx` - Detection controls and results display
- `ProjectConflicts.tsx` - Full-page conflict management view
- Route: `/projects/:id/conflicts`

### Win Probability ML System

**Feature Engineering**
- Extracts 8 key predictive features from project data:
  - Project Type Score - Alignment with company expertise
  - Client Relationship Score - Historical relationship strength
  - Competitiveness Score - Competitive positioning
  - Team Capacity Score - Resource availability
  - Timeline Score - Deadline feasibility
  - Complexity Score - Project complexity assessment
  - Requirements Clarity Score - RFP clarity level
  - Budget Alignment Score - Budget-scope fit
- Historical win rate integration from past bids with same client

**Statistical Scoring Model**
- Weighted feature scoring with configurable weights
- Sigmoid transformation for probability output
- Confidence scoring based on data quality and historical data
- Risk and strength factor identification
- Actionable recommendations generation

**Database Tables**
- `win_probability_predictions` - Stores predictions with feature scores
- `bid_outcomes` - Records actual bid outcomes for model feedback
- `project_features` - Cached extracted features per project

**API Endpoints**
- `POST /api/win-probability/predict/:projectId` - Generate new prediction
- `GET /api/win-probability/prediction/:projectId` - Get latest prediction
- `GET /api/win-probability/history/:projectId` - Get prediction history
- `GET /api/win-probability/features/:projectId` - Get extracted features
- `POST /api/win-probability/outcome/:projectId` - Record bid outcome
- `GET /api/win-probability/metrics` - Get model performance metrics
- `GET /api/win-probability/stats` - Get aggregate statistics

**Frontend Components**
- `WinProbability.tsx` - Probability display with feature breakdown
- Integrated into ProjectAnalysis page

### External Dependencies

**AI Services**
- OpenAI API for GPT-4o completions and text embeddings
- Anthropic API for Claude Sonnet 4.5 completions
- Google Gemini API for Gemini 2.5 Flash completions
- All three providers configurable via environment variables with custom base URLs

**Database**
- Neon serverless PostgreSQL (or compatible PostgreSQL service)
- Requires pgvector extension for vector similarity search
- Connection via `DATABASE_URL` environment variable

**Development Tools**
- Replit-specific plugins for Vite (cartographer, dev banner, runtime error modal, meta images)
- ESBuild for server-side bundling with selective dependency bundling

**File Processing**
- Multer for multipart form uploads
- In-memory storage strategy for uploaded files
- Support for PDF, MSG, and ZIP file formats (processing implementation pending)

**Build & Deployment**
- Separate build processes for client (Vite) and server (ESBuild)
- Production deployment serves static assets from Express
- Client built to `dist/public`, server built to `dist/index.cjs`
- Environment-based configuration (NODE_ENV, REPL_ID)