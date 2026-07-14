# RootCause AI

An AI-powered Incident Response Platform that helps engineering teams investigate production incidents by uploading logs and generating AI-assisted root cause analysis.

The platform enables engineers to create incidents, upload application logs, and receive intelligent summaries, probable root causes, suggested fixes, and follow-up actions using Google's Gemini AI.

---

# Project Status

Current Version: **v1.0**

Completed:
- Incident Management
- Log Upload
- AI Root Cause Analysis
- PostgreSQL Integration
- REST APIs
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
- Deployment 

---

# Author

**Priyanshi Saxena**
