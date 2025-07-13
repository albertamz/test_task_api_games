import pytest
from users.models import User, UserToken


@pytest.fixture
def user_and_token(db):
    user = User.objects.create_user(username="apiuser", phone_number="380000000000")
    token = UserToken.objects.create(user=user)
    return user, str(token.token)


@pytest.mark.django_db
def test_user_register(client):
    response = client.post("/user/register", {
        "username": "newuser",
        "phone_number": "380123456789"
    })

    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert "token" in data
    assert "token_expires_at" in data


@pytest.mark.django_db
def test_token_info(client, user_and_token):
    _, token = user_and_token
    response = client.get(f"/game/{token}")
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "username" in data
    assert "phone_number" in data


@pytest.mark.django_db
def test_token_renew(client, user_and_token):
    _, token = user_and_token
    response = client.post(f"/game/{token}/renew")
    assert response.status_code == 200
    data = response.json()
    assert "new_token" in data
    assert "token_expires_at" in data


@pytest.mark.django_db
def test_token_deactivate(client, user_and_token):
    _, token = user_and_token
    response = client.post(f"/game/{token}/deactivate")
    assert response.status_code == 200
    assert response.json()["message"] == "Token deactivated"


@pytest.mark.django_db
def test_game_play(client, user_and_token):
    _, token = user_and_token
    response = client.post(f"/game/{token}/play")
    assert response.status_code == 201
    data = response.json()
    assert 1 <= data["number"] <= 1000
    assert data["result"] in ["win", "lose"]
    assert isinstance(data["prize"], float)


@pytest.mark.django_db
def test_game_history(client, user_and_token):
    _, token = user_and_token

    for _ in range(5):
        client.post(f"/game/{token}/play")

    response = client.get(f"/game/{token}/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 3
    for item in data:
        assert "number" in item
        assert "result" in item
        assert "prize" in item
        assert "played_at" in item
        assert "win" in item
