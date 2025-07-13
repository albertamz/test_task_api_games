import pytest
from users.models import User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username="testuser", phone_number="380000000000")
    assert user.username == "testuser"
    assert user.phone_number == "380000000000"
    assert user.is_active
    assert not user.is_staff
    assert not user.has_usable_password()
    assert str(user) == "testuser"


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(username="admin", phone_number="380999999999")
    assert user.is_superuser
    assert user.is_staff
    assert str(user) == "admin"
