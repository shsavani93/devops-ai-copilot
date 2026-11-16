import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()

def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "devops-ai-copilot"
    }


def test_create_log(client):
    payload = {
        "service": "payment-api",
        "level": "ERROR",
        "message": "Database connection timeout",
        "timestamp": "2026-11-13T10:30:00Z"
    }

    response = client.post("/api/v1/logs", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["service"] == "payment-api"
    assert data["level"] == "ERROR"
    assert data["log_message"] == "Database connection timeout"
    assert data["id"] is not None

def test_create_log_invalid_payload(client):
    payload = {
        "service": "payment-api",
        "level": "INVALID_LEVEL",
        "message": "",
        "timestamp": "not-a-valid-date"
    }

    response = client.post("/api/v1/logs", json=payload)

    assert response.status_code == 422

def test_get_logs(client):
    payload = {
        "service": "payment-api",
        "level": "ERROR",
        "message": "Database connection timeout",
        "timestamp": "2026-11-13T10:30:00Z"
    }

    client.post("/api/v1/logs", json=payload)

    response = client.get("/api/v1/logs")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["service"] == "payment-api"
    assert data[0]["level"] == "ERROR"
