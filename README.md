# RootCause AI

An AI-powered Incident Response Platform that helps engineering teams analyze production incidents, identify possible root causes using Retrieval-Augmented Generation (RAG), summarize logs, and accelerate incident resolution.

---

## Overview

RootCause AI is designed to reduce the time engineers spend investigating production issues.

The platform allows users to create incidents, upload logs, retrieve relevant historical incidents and documentation, and generate AI-assisted root cause analysis using Large Language Models (LLMs).

Instead of manually reading thousands of log lines, engineers receive concise summaries, possible causes, and recommended next steps.

---

## Features

- Incident Management
  - Create incidents
  - Track incident status
  - Assign severity
  - Environment support (Production, Staging, Development)

- AI Investigation
  - AI-generated incident summary
  - Root cause prediction
  - Suggested troubleshooting steps

- Retrieval-Augmented Generation (RAG)
  - Searches previous incidents
  - Retrieves documentation
  - Uses relevant context before generating answers

- Log Analysis
  - Upload logs
  - AI extracts important errors
  - Highlights anomalies

- REST API
  - FastAPI backend
  - Swagger documentation

---

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

### AI

- LangChain
- OpenAI
- ChromaDB
- Sentence Transformers

### DevOps

- Docker
- Docker Compose
- GitHub Actions
- Nginx

### Cloud (Planned)

- AWS
- Azure

---

## Project Structure

rootcause-ai/
│
├── app/
│ ├── api/
│ ├── models/
│ ├── schemas/
│ ├── services/
│ ├── database/
│ └── main.py
│
├── data/
├── vectorstore/
├── tests/
├── docker/
├── requirements.txt
├── Dockerfile
└── README.md

# Getting Started

## Clone Repository

```bash
git clone https://github.com/yourusername/rootcause-ai.git
```

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Server

```bash
uvicorn app.main:app --reload
```

---

# API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Current API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Health Check |
| POST | /incidents | Create Incident |
| GET | /incidents | List Incidents |
| GET | /incidents/{id} | Get Incident |
| PUT | /incidents/{id} | Update Incident |
| DELETE | /incidents/{id} | Delete Incident |

---

# Current Progress

## Phase 1 – Backend Foundation 

- [x] Repository setup
- [x] FastAPI project initialization
- [x] Virtual environment
- [x] PostgreSQL connection
- [x] SQLAlchemy configuration
- [x] Database models
- [x] Pydantic schemas
- [x] CRUD APIs
- [x] Swagger documentation

---

## Phase 2 – In Progress 

- [ ] Alembic migrations
- [ ] Log upload API
- [ ] File storage
- [ ] Error handling
- [ ] API validation

---

## Phase 3 – AI Integration

- [ ] Document ingestion
- [ ] Embedding generation
- [ ] ChromaDB integration
- [ ] LangChain pipeline
- [ ] RAG implementation
- [ ] AI root cause generation

---

## Phase 4 – Production Ready

- [ ] Docker
- [ ] Docker Compose
- [ ] Unit testing
- [ ] CI/CD pipeline
- [ ] Deployment
- [ ] Monitoring

---

# Roadmap

- AI-powered log analysis
- Semantic search
- Historical incident retrieval
- Authentication
- Dashboard
- Kubernetes deployment
- Monitoring with Prometheus
- Grafana dashboards
- AWS deployment

---

# Learning Outcomes

This project demonstrates practical experience with:

- Backend Development
- REST APIs
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- GitHub Actions
- Retrieval-Augmented Generation (RAG)
- Vector Databases
- LangChain
- Prompt Engineering
- System Design
- AI-assisted DevOps

