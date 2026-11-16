# DevOps AI Copilot

An AI-powered incident investigation platform that analyzes application logs, identifies potential root causes, and generates evidence-backed remediation recommendations.

## Overview

DevOps AI Copilot aims to reduce the time engineers spend investigating production incidents by combining log analysis, AI-powered reasoning, and retrieval-augmented generation (RAG).

The platform will help engineers:
- Ingest and store application logs.
- Identify and group related errors into incidents.
- Investigate incidents using relevant logs and technical documentation.
- Generate evidence-backed root cause analyses.
- Recommend remediation steps with supporting evidence.
- Require human approval before applying any code changes.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| API validation | Pydantic |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.x |
| Local infrastructure | Docker Compose |
| Testing | Pytest, FastAPI TestClient |
| AI/LLM | Planned |
| Vector search / RAG | Planned |
| Frontend | Planned |

## Current Implementation

### Backend
- FastAPI application with health-check endpoint.
- Log ingestion API.
- Request validation using Pydantic.
- PostgreSQL integration using SQLAlchemy.
- Persistent application log storage.
- Log retrieval with optional service and severity filters.
- Pagination using `skip` and `limit`.
- Explicit API response schemas.
- Database transaction rollback and error handling.

### Testing
- Automated API tests using pytest.
- Health-check endpoint testing.
- Log creation testing.
- Invalid request validation testing.
- Log retrieval testing.
- Isolated in-memory SQLite test database.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check application health |
| POST | `/api/v1/logs` | Ingest an application log |
| GET | `/api/v1/logs` | Retrieve application logs |

### Example: Ingest a log

**Request**

```http
POST /api/v1/logs
Content-Type: application/json
```

```json
{
  "service": "payment-api",
  "level": "ERROR",
  "message": "Payment processing failed due to database timeout",
  "timestamp": "2026-11-13T10:30:00Z"
}
```

**Response**

```json
{
  "id": 1,
  "message": "Log stored successfully",
  "service": "payment-api",
  "level": "ERROR",
  "log_message": "Payment processing failed due to database timeout",
  "timestamp": "2026-11-13T10:30:00Z"
}
```

### Example: Retrieve logs

```http
GET /api/v1/logs
```

Optional query parameters:

- `service`: Filter by application service.
- `level`: Filter by log severity.
- `skip`: Number of records to skip.
- `limit`: Maximum records to return (1–100).

Example:

```http
GET /api/v1/logs?service=payment-api&level=ERROR&skip=0&limit=20
```

## Local Development Setup

### Prerequisites

- Python 3.12+
- Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd devops-ai-copilot
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Update `.env` with your local PostgreSQL configuration.

### 3. Start PostgreSQL

```bash
docker compose up -d postgres
```

### 4. Set up the Python environment

```bash
cd backend

python3.12 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 5. Initialize database tables

```bash
python -m app.db.init_db
```

### 6. Start the FastAPI server

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Swagger documentation: http://127.0.0.1:8000/docs

## Running Tests

From the `backend` directory:

```bash
python -m pytest -v
```

The automated tests use an isolated in-memory SQLite database and do not modify the development PostgreSQL database.

## Planned Features

- Incident detection and error grouping.
- AI-powered incident investigation.
- Retrieval-augmented generation (RAG) using historical logs and technical documentation.
- Vector search using pgvector.
- Evidence-backed root cause analysis.
- Structured remediation recommendations.
- Human-in-the-loop approval workflow.
- Background processing for large log volumes.
- Frontend dashboard for incident investigation.

## Design Principles

- Evidence-backed AI recommendations.
- Separation of API, business logic, and persistence layers.
- Reliable database transactions.
- Input and output validation.
- Automated testing.
- Human approval before executing remediation actions.

---

**Project Status:** Backend foundation implemented; AI investigation capabilities are under development.
