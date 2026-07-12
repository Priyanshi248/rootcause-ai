# RootCause AI

An AI-powered Incident Response Platform that helps engineering teams investigate production incidents by uploading logs and generating AI-assisted root cause analysis.

The platform enables engineers to create incidents, upload application logs, and receive intelligent summaries, probable root causes, suggested fixes, and follow-up actions using Google's Gemini AI.

---

# Project Status

**Currently Under Active Development**

Current Version: **v1.0**

Completed:
- Incident Management
- Log Upload
- AI Root Cause Analysis
- PostgreSQL Integration
- REST APIs

Upcoming:
- RAG Pipeline
- AI Chat Assistant
- Authentication
- Dashboard
- Docker Deployment
- CI/CD

---

# Features

## Incident Management

- Create incidents
- View all incidents
- View incident details
- Update incidents
- Delete incidents
- Track severity
- Track environment
- Track incident status

---

## Log Management

- Upload log files
- Store logs in PostgreSQL
- Associate logs with incidents

---

## AI Analysis

Using **Google Gemini**, the platform generates:

- Incident Summary
- Root Cause Analysis
- Suggested Fixes
- Follow-up Actions

AI responses are automatically stored for future reference.

---

## REST APIs

Interactive API documentation using Swagger UI.

Available endpoints include:

- Incident APIs
- Log APIs
- AI Analysis APIs

---

# Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Alembic

## AI

- Google Gemini API
- Prompt Engineering

## Tools

- Swagger UI
- Git
- GitHub
- Pydantic

---

# Current API Endpoints

## Incident APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /incidents | Create Incident |
| GET | /incidents | List Incidents |
| GET | /incidents/{id} | Get Incident |
| PUT | /incidents/{id} | Update Incident |
| DELETE | /incidents/{id} | Delete Incident |

---

## Log APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /logs/upload | Upload Logs |

---

## AI APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /analysis/{incident_id} | Generate AI Root Cause Analysis |

---

# Current Progress

## Phase 1 – Backend Foundation ✅

- [x] FastAPI Setup
- [x] PostgreSQL Integration
- [x] SQLAlchemy Async
- [x] Alembic Migrations
- [x] Database Models
- [x] Repository Pattern
- [x] Service Layer
- [x] CRUD APIs
- [x] Swagger Documentation

---

## Phase 2 – AI Integration ✅

- [x] Log Upload
- [x] Gemini API Integration
- [x] Prompt Engineering
- [x] AI Root Cause Analysis
- [x] Store AI Results
- [x] Cascade Delete
- [x] Error Handling

---

## Phase 3 – In Progress 🚧

- [ ] Dashboard APIs
- [ ] Incident Timeline
- [ ] AI Chat
- [ ] Historical Incident Search

---

## Phase 4 – RAG Pipeline

- [ ] Document Ingestion
- [ ] Embeddings
- [ ] Vector Database
- [ ] Semantic Search
- [ ] Retrieval-Augmented Generation

---

## Phase 5 – Production Ready

- [ ] JWT Authentication
- [ ] Docker
- [ ] Docker Compose
- [ ] GitHub Actions
- [ ] Unit Tests
- [ ] Deployment
- [ ] Monitoring

---

# Project Structure

```
backend/
│
├── alembic/
├── app/
│   ├── api/
│   ├── agents/
│   ├── core/
│   ├── db/
│   ├── enums/
│   ├── mixins/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── uploads/
├── requirements.txt
└── README.md
```

---

# Future Enhancements

- AI Chat Assistant
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Historical Incident Retrieval
- Authentication & Authorization
- Incident Dashboard
- Docker Deployment
- CI/CD Pipeline
- Kubernetes Deployment
- AWS / Azure Hosting

---

# Learning Outcomes

This project demonstrates hands-on experience with:

- FastAPI
- Python
- Async SQLAlchemy
- PostgreSQL
- Alembic
- REST API Design
- Repository Pattern
- Service Layer Architecture
- Prompt Engineering
- Google Gemini API
- Production Incident Management
- AI-powered Backend Development

---

# Author

**Priyanshi Saxena**
