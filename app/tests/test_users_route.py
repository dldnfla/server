from .. import crud, oauth2


def test_create_user_success(client, session, username, password):
    body = {"username": username, "password": password}

    response = client.post(
        "/users/",
        json=body,
    )

    assert response.status_code == 201, response.text

    data = response.json()
    assert data["username"] == username

    user = crud.get_user_by_username(session, username)
    assert oauth2.verify_password(password, user.hashed_password)


def test_create_user_fail(client, test_user):
    response = client.post(
        "/users/",
        json={
            "username": test_user["username"],
            "password": "asdf",
        },
    )

    assert response.status_code == 400, response.text


def test_update_user_success(authorized_client):
    response = authorized_client.put(
        "/users/me", json={"fullname": "1234", "statusmessage": "asdf"}
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["fullname"] == "1234"
    assert data["status_message"] == "asdf"
