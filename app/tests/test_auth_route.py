username = "test"
password = "test_password"


def test_token_success(client):
    response = client.post(
        "/users/",
        json={
            "username": username,
            "password": password,
        },
    )
    assert response.status_code == 201, response.text

    response = client.post(
        "/auth/token", data={"username": username, "password": password}
    )

    assert response.status_code == 200, response.text


def test_token_wrong_password(client):
    response = client.post(
        "/auth/token", data={"username": username, "password": password + "a"}
    )

    assert response.status_code == 401, response.text
