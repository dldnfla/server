import copy
import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .. import crud, oauth2, schemas
from ..database import Base, get_db
from ..main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def username():
    return "test@example.com"


@pytest.fixture
def password():
    return "fakepassword"


@pytest.fixture()
def test_user(client, email, password):
    body = {"email": email, "password": password}

    response = client.post("/users/", json=body)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == body["email"]
    data["password"] = body["password"]

    return data


@pytest.fixture()
def authenticated_user(client, test_user):
    response = client.post(
        "/auth/token",
        data={"email": test_user["email"], "password": test_user["password"]},
    )

    assert response.status_code == 201, response.text


@pytest.fixture
def test_todos(test_user, session):
    todos = []
    for t in range(10):
        todo = crud.create_todo(
            session,
            schemas.TodoCreate(
                date=datetime.datetime(2023, 11, 23, t, 24, 10),
                icon="iconname",
                title=f"title_{t}",
                contents=f"content_{t}",
                color="#FFFFFF",
                done=False,
            ),
            user_id=test_user["id"],
        )

        todos.append(todo)

    return todos


@pytest.fixture
def token(test_user):
    return oauth2.create_access_token({"sub": test_user["email"]})


@pytest.fixture
def authorized_client(session, token):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    yield client


@pytest.fixture
def test_todo(authorized_client):
    response = authorized_client.post(
        "/todos/",
        json={
            "date": str(datetime.datetime(2023, 11, 23, 1, 24, 10)),
            "icon": "iconname",
            "title": "title",
            "contents": "content",
            "color": "#FFFFFF",
            "done": False,
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    return data
