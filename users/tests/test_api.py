import pytest
from users.models import User


@pytest.mark.django_db
def test_register_success(client):
    response = client.post("/user/register", {
        "username": "newbie",
        "phone_number": "380666666666"
    })
    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert "token" in data
    assert "token_expires_at" in data

    assert User.objects.filter(username="newbie").exists()


@pytest.mark.django_db
def test_register_duplicate_username(client):
    User.objects.create_user(username="repeat", phone_number="380123456789")

    response = client.post("/user/register", {
        "username": "repeat",
        "phone_number": "380111111111"
    })
    assert response.status_code == 400
    assert "Username already exists" in str(response.content)


@pytest.mark.django_db
def test_register_duplicate_phone(client):
    User.objects.create_user(username="uniq", phone_number="380999999999")

    response = client.post("/user/register", {
        "username": "newuser",
        "phone_number": "380999999999"
    })
    assert response.status_code == 400
    assert "Phone number already exists" in str(response.content)
