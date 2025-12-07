# BidForge AI

Construction Bidding Automation System powered by AI

## Overview

BidForge AI streamlines the proposal generation process for construction companies. The application ingests RFQ documents (PDFs, emails, ZIP files), uses Retrieval-Augmented Generation (RAG) with vector search to find relevant context from current and historical projects, and generates professional HTML bid responses using AI.

## Features

- **Multi-AI Provider Support**: OpenAI (GPT-4o), Anthropic (Claude Sonnet 4.5), Google Gemini
- **Intelligent Document Processing**: Upload and analyze RFQ documents
- **RAG-Powered Context**: Vector search for relevant historical data
- **RFP Risk Assessment**: AI-powered scoring and analysis
- **Project Dashboard**: Track active, submitted, and closed projects
- **Win Rate Analytics**: Monitor bid performance

## Tech Stack

**Frontend:**
- React 19 + TypeScript
- Vite
- Tailwind CSS v4
- Shadcn UI Components
- TanStack Query
- Wouter (routing)
- Zustand (state management)

**Backend:**
- Express + TypeScript
- Drizzle ORM
- Neon PostgreSQL + pgvector
- JWT Authentication
- Multi-AI Integration

## Prerequisites

- Node.js 18+
- PostgreSQL with pgvector extension (or Neon serverless)
- API keys for AI providers (OpenAI, Anthropic, and/or Google)

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# Database (use Neon serverless or local PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/bidforge

# AI Providers (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# JWT Secrets (generate secure random strings)
JWT_SECRET=your-secure-secret-here
JWT_REFRESH_SECRET=your-secure-refresh-secret-here

# Server
PORT=3000
NODE_ENV=development
```

### 3. Setup Database

Ensure your PostgreSQL database has the pgvector extension:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Push the database schema:

```bash
npm run db:push
```

### 4. Run Development Servers

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
npm run dev
```

**Terminal 2 - Frontend:**
```bash
npm run dev:client
```

Visit `http://localhost:5000`

## Production Build

Build the application for production:

```bash
npm run build
```

Start the production server:

```bash
npm start
```

## Project Structure

```
BidForgeAI/
├── client/              # React frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Page components
│   │   ├── lib/         # API client, utilities
│   │   └── hooks/       # Custom React hooks
│   └── index.html
├── server/              # Express backend
│   ├── routes/          # API routes
│   ├── services/        # AI services
│   ├── middleware/      # Auth middleware
│   └── index.ts         # Server entry point
├── shared/              # Shared types & schema
│   ├── schema.ts        # Drizzle database schema
│   └── types.ts         # TypeScript types
└── script/              # Build scripts
```

## Available Scripts

- `npm run dev` - Start development backend server
- `npm run dev:client` - Start development frontend (Vite)
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run check` - TypeScript type checking
- `npm run db:push` - Push database schema changes

## API Documentation

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user

### Projects

- `POST /api/projects` - Create project
- `GET /api/projects` - Get all user projects
- `GET /api/projects/:id` - Get project details
- `PATCH /api/projects/:id` - Update project
- `DELETE /api/projects/:id` - Delete project

### Documents

- `POST /api/documents/upload/:projectId` - Upload document
- `GET /api/documents/:id` - Get document
- `DELETE /api/documents/:id` - Delete document

### Bids

- `POST /api/bids/generate` - Generate bid with AI
- `GET /api/bids/history/:projectId` - Get bid history
- `POST /api/bids/analyze/:projectId` - Analyze RFP
- `GET /api/bids/analysis/:projectId` - Get latest analysis

## License

MIT