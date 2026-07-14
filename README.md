# RootCause AI

An AI-powered Incident Management Platform that combines Retrieval-Augmented Generation (RAG) with Large Language Models to automate root cause analysis, incident investigation, and remediation suggestions for engineering teams.

RootCause AI enables developers and DevOps teams to upload production incidents, analyze system logs using AI, retrieve similar historical incidents through vector search, and generate actionable debugging insights—all from a single platform.

---

## Features

- AI-powered root cause analysis using LLMs
- Retrieval-Augmented Generation (RAG) for historical incident lookup
- Incident lifecycle management
- AI-generated summaries and suggested fixes
- Semantic search over previous incidents
- JWT Authentication
- Incident timeline tracking
- Dockerized backend
- RESTful API built with FastAPI
- PostgreSQL database with Alembic migrations

---

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic

### Database

- PostgreSQL

### AI

- OpenRouter API
- LLMs (Gemini / Nemotron / OpenAI compatible)
- ChromaDB
- Retrieval-Augmented Generation (RAG)

### DevOps

- Docker
- Docker Compose

### Authentication

- JWT

---

# System Architecture

```
                        User
                         │
                         ▼
                  FastAPI Backend
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
 Authentication    Incident APIs     AI Analysis
        │                │                │
        ▼                ▼                ▼
 PostgreSQL        ChromaDB        OpenRouter LLM
        │                │                │
        └───────────────RAG───────────────┘
                         │
                         ▼
               Root Cause Analysis
```

---

# Features

## Authentication

- User registration
- Login
- JWT authentication
- Protected APIs

---

## Incident Management

Users can

- Create incidents
- View incidents
- Update incidents
- Delete incidents
- Track incident history

Each incident stores

- Title
- Description
- Severity
- Status
- Timestamp

---

## AI Incident Analysis

The AI engine automatically analyzes uploaded incident descriptions and generates

- Executive Summary
- Root Cause
- Suggested Fix
- Follow-up Actions

Example

```
Summary:
Database timeout caused API failures.

Root Cause:
Missing database index on frequently queried column.

Suggested Fix:
Create index and optimize slow query.

Follow-up:
Monitor query latency after deployment.
```

---

## Retrieval-Augmented Generation (RAG)

Before generating a response, RootCause AI searches previous incidents stored in a vector database.

The retrieved context is combined with the current incident before sending it to the LLM.

Benefits

- Better contextual responses
- Reduced hallucinations
- Consistent troubleshooting
- Knowledge reuse

---

## Semantic Search

Historical incidents are embedded into ChromaDB.

Similar incidents can be retrieved using semantic similarity instead of keyword matching.

---

## Incident Timeline

Every AI analysis is stored separately, allowing teams to

- Track incident evolution
- Compare analyses
- Review previous recommendations

---

## Database

Main entities include

### Users

- id
- username
- email
- password

### Incidents

- id
- title
- description
- severity
- status
- created_at

### AI Analysis

- id
- incident_id
- summary
- root_cause
- suggested_fix
- follow_up_actions

---

# Project Structure

```
RootCause-AI/
│
├── app/
│   ├── api/
│   ├── agents/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── schemas/
│   ├── db/
│   └── core/
│
├── chroma_db/
├── alembic/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/Priyanshi248/rootcause-ai.git
```

Move into the project

```bash
cd rootcause-ai
```

Create environment variables

```env
DATABASE_URL=

OPENROUTER_API_KEY=

JWT_SECRET_KEY=
```

Run with Docker

```bash
docker compose up --build
```

Run locally

```bash
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Swagger UI

```
http://localhost:8000/docs
```

---

# Workflow

1. User creates an incident.
2. Incident is stored in PostgreSQL.
3. Logs are embedded into ChromaDB.
4. Similar historical incidents are retrieved.
5. Context is sent to the LLM.
6. AI generates:

- Summary
- Root Cause
- Suggested Fix
- Follow-up Actions

7. Analysis is saved.
8. User can review previous analyses.

---

# Future Enhancements

- Frontend dashboard using React
- Grafana monitoring
- Kubernetes deployment
- CI/CD with GitHub Actions
- Multi-agent architecture
- Elasticsearch integration
- Slack & Microsoft Teams notifications
- Prometheus metrics
- Redis caching
- RBAC (Role-Based Access Control)

---

# Author

**Priyanshi Saxena**
