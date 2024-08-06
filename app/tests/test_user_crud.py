from .. import crud, schemas


def test_create_user(email, password, session):
    response = crud.create_user(
        session,
        schemas.UserCreate(
            email="hi",
            password=password,
        ),
    )

    assert response.email == "hi"


def test_get_user(email, password, session):
    email = email + "a"

    crud.create_user(
        session,
        schemas.UserCreate(
            email=email,
            password=password,
        ),
    )

    user = crud.get_user_by_email(session, email)

    assert user.email == email
