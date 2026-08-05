from collections.abc import Generator
from os import environ

environ.setdefault("DATABASE_URL", "sqlite://")

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import User

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_register_login_refresh_and_me_flow() -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "khushi",
            "email": "khushi@example.com",
            "password": "strong-password",
        },
    )
    assert register_response.status_code == 201
    register_data = register_response.json()
    assert register_data["user"]["email"] == "khushi@example.com"
    assert register_data["access_token"]
    assert register_data["refresh_token"]

    me_response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {register_data['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "khushi"

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "khushi", "password": "strong-password"},
    )
    assert login_response.status_code == 200
    login_data = login_response.json()

    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": login_data["refresh_token"]},
    )
    assert refresh_response.status_code == 200
    assert refresh_response.json()["access_token"]


def test_duplicate_registration_is_rejected() -> None:
    payload = {
        "username": "khushi",
        "email": "khushi@example.com",
        "password": "strong-password",
    }

    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 409


def test_admin_route_requires_admin_role() -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "khushi",
            "email": "khushi@example.com",
            "password": "strong-password",
        },
    )
    token = register_response.json()["access_token"]

    forbidden_response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert forbidden_response.status_code == 403

    with TestingSessionLocal() as db:
        user = db.query(User).filter(User.email == "khushi@example.com").one()
        user.role = "admin"
        db.commit()

    admin_response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert admin_response.status_code == 200
    assert len(admin_response.json()) == 1
