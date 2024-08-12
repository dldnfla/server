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
    return "username"


@pytest.fixture
def password():
    return "fakepassword"


@pytest.fixture()
def test_user(client, username, password):
    body = {"username": username, "password": password}

    response = client.post("/users/signup", json=body)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["username"] == body["username"]
    data["password"] = body["password"]

    return data


@pytest.fixture()
def authenticated_user(client, test_user):
    response = client.post(
        "/auth/token",
        data={"username": test_user["username"], "password": test_user["password"]},
    )

    assert response.status_code == 201, response.text


@pytest.fixture
def token(test_user):
    return oauth2.create_access_token({"sub": test_user["username"]})


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
def test_dialogs(session):
    dialogs = []
    for t in range(10):
        dialog = crud.create_dialog(
            session,
            schemas.DialogCreate(
                user_id=1,
                visitor="tester",
                contents=f"{t}th testing",
            ),
        )

        dialogs.append(dialog)

    return dialogs


@pytest.fixture
def test_dialog(authorized_client):
    response = authorized_client.post(
        "/dialog/",
        json={
            "user_id": 1,
            "visitor": "tester",
            "contents": "testing",
        },
    )

    assert response.status_code == 201, response.text
    data = response.json()

    return data


@pytest.fixture
def test_qna_answer(session):
    qna = crud.create_qna(
        session,
        schemas.QnaCreate(
            user_id="test_user",
            answer1="answer1",
            answer2="answer2",
            answer3="answer3",
            answer4="answer4",
            answer5="answer5",
            answer6="answer6",
            answer7="answer7",
            answer8="answer8",
            answer9="answer9",
            answer10="answer10",
        ),
    )
    session.commit()
    
    return qna

@pytest.fixture
def test_qna(session):
    qna = crud.update_qna(
        session,
        schemas.QnaEdit(
            answer1="answer1",
            answer2="answer2",
            answer3="answer3",
            answer4="answer4",
            answer5="answer5",
            answer6="answer6",
            answer7="answer7",
            answer8="answer8",
            answer9="answer9",
            answer10="answer10",
        ),
        user_id= "test_user"
    )
    session.commit()
    
    return qna


# @pytest.fixture
# def test_qna(authorized_client):
#     response = authorized_client.post(
#         "/qna/",
#         json={
#             "answer1": "testanswer1",
#             "answer2": "testanswer2",
#             "answer3": "testanswer3",
#             "answer4": "testanswer4",
#             "answer5": "testanswer5",
#             "answer6": "testanswer6",
#             "answer7": "testanswer7",
#             "answer8": "testanswer8",
#             "answer9": "testanswer9",
#             "answer10": "testanswer10",
#         },
#     )

    assert response.status_code == 201, response.text
    data = response.json()

    return data