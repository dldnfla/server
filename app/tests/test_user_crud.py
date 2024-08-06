from .. import crud, schemas


def test_create_user(username, password, session):
    response = crud.create_user(
        session,
        schemas.UserCreate(
            username=username,
            password=password,
        ),
    )

    assert response.username == username


def test_get_user(username, password, session):
    username = username + "a"

    crud.create_user(
        session,
        schemas.UserCreate(
            username=username,
            password=password,
        ),
    )

    user = crud.get_user_by_username(session, username)

    assert user.username == username
