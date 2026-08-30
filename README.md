# RootCause AI

**RootCause AI** is an AI-powered incident intelligence platform designed to help engineering and DevOps teams investigate production incidents, identify potential root causes, retrieve similar historical incidents, and generate actionable remediation suggestions.

The platform combines **Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), vector search, incident management, operational logs, and AI-assisted investigation** into a single application.

---

## Live Demo

| Service                 | Link                                           |
| ----------------------- | ---------------------------------------------- |
| **Live Application** | https://rootcause-ai-sand.vercel.app/          |
| **Backend API**      | https://rootcause-ai-backend.onrender.com/     |
| **Swagger API Docs** | https://rootcause-ai-backend.onrender.com/docs |

---

## Features

### Authentication

* User registration and login
* JWT-based authentication
* Secure password hashing using bcrypt

### Incident Management

* Create, view, and update incidents
* Track incident severity and status
* Store incident descriptions and timestamps
* Manage the complete incident lifecycle

### AI Incident Analysis

AI-powered analysis generates structured insights such as:

* Executive summary
* Possible root cause
* Suggested fixes
* Follow-up actions
* Relevant historical incidents

### Retrieval-Augmented Generation

RootCause AI uses **RAG** to retrieve relevant historical incidents before generating AI responses.

This allows the system to use previously resolved incidents as contextual knowledge when investigating new incidents.

### AI Assistant

The integrated AI Assistant allows users to ask questions about:

* Production incidents
* Operational issues
* Historical incidents
* Possible causes
* Recommended remediation steps

### Dashboard

The dashboard provides an overview of the operational state of the system, including:

* Total incidents
* Incident severity
* Incident status
* Incident activity

### Operational Logs

RootCause AI supports multiple log categories:

* Application
* Nginx
* Docker
* Kubernetes
* System
* Custom

Logs can be used during incident investigation and AI-assisted analysis.

### Incident Timeline

The incident timeline provides a chronological view of an incident from detection to resolution.

```text
Incident Detected
       ↓
Investigation Started
       ↓
Logs Reviewed
       ↓
AI Analysis
       ↓
Remediation
       ↓
Incident Resolved
```

### Audit Logs

Important system activities are recorded through audit logs.

This improves **traceability, accountability, and visibility** during incident investigation and management.

---

## RAG Workflow

The RAG pipeline retrieves relevant historical information using semantic similarity and provides it as context to the language model.

```text
User Question / Incident
          ↓
     Generate Embedding
          ↓
      Vector Search
          ↓
Historical Incidents
          ↓
    Relevant Context
          ↓
         LLM
          ↓
   AI Generated Response
```

---

## Semantic Search

Historical incident information is converted into vector embeddings and stored in **ChromaDB**.

When a new incident or question is analyzed, RootCause AI searches for semantically similar historical incidents rather than relying only on exact keyword matches.

For example:

```text
New Incident:
"API requests are timing out"

Historical Incident:
"Backend requests experienced high latency"

                ↓

       Semantic Similarity Search

                ↓

   Relevant Historical Incident
```

This allows the system to retrieve useful incidents even when their wording is different.

---

## System Architecture

```text
                         User
                           │
                           ↓
                   Vercel Frontend
                           │
                           ↓
                    FastAPI Backend
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
       PostgreSQL       ChromaDB      OpenRouter
          Neon           Vectors          LLM
             │             │             │
             └─────────────┼─────────────┘
                           ↓
                     RAG Pipeline
                           ↓
                  AI Incident Analysis
                           ↓
                Root Cause + Remediation
```

---

## Tech Stack

### Frontend

* HTML
* CSS
* JavaScript
* Vercel

### Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic
* JWT Authentication
* bcrypt

### Database

* PostgreSQL
* Neon PostgreSQL

### AI & RAG

* OpenRouter
* Large Language Models
* Hugging Face Embeddings
* ChromaDB
* Semantic Search
* Retrieval-Augmented Generation

### DevOps

* Docker
* Docker Compose
* GitHub Actions
* Render
* Vercel

---

## CI/CD

RootCause AI uses **GitHub Actions** to automatically execute backend tests when changes are pushed to the repository.

The automated tests cover areas such as:

* Database connectivity
* Model imports
* ChromaDB retrieval
* AI response parsing

### CI/CD Workflow

```text
Git Push
   ↓
GitHub Actions
   ↓
Automated Tests
   ↓
Deployment
```

---

## Docker

The backend is containerized using Docker to provide a consistent development and deployment environment.

Start the application using:

```bash
docker compose up --build
```

---

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Priyanshi248/rootcause-ai.git
cd rootcause-ai
```

### 2. Move to the Backend

```bash
cd backend
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file containing the required configuration for:

* PostgreSQL database
* JWT authentication
* OpenRouter / AI API
* ChromaDB
* Other application settings

Example:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
OPENROUTER_API_KEY=your_api_key
```

> Never commit your `.env` file or API keys to GitHub.

### 5. Run the Backend

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

### 6. Open Swagger Documentation

```text
http://localhost:8000/docs
```

### 7. Run Tests

```bash
pytest -q
```

---

## Deployment

RootCause AI uses separate services for production deployment.

```text
Frontend  → Vercel
Backend   → Render
Database  → Neon PostgreSQL
CI/CD     → GitHub Actions
```

The frontend communicates with the FastAPI backend through REST APIs.

---

## Project Structure

```text
rootcause-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## Why RootCause AI?

Traditional incident investigation often requires engineers to manually search through logs, previous incidents, documentation, and monitoring systems.

RootCause AI brings these capabilities together and uses AI + historical incident retrieval to help engineers move from:

```text
Incident
   ↓
Investigation
   ↓
Historical Context
   ↓
Possible Root Cause
   ↓
Remediation
```

The goal is to **reduce investigation time, improve incident response, and preserve organizational knowledge from previous incidents.**
