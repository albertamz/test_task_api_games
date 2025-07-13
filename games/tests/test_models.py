import pytest
from datetime import timedelta
from django.utils import timezone
from users.models import User, UserToken
from games.models import GameResult


@pytest.mark.django_db
def test_usertoken_valid_and_str():
    user = User.objects.create_user(username="modeluser", phone_number="380111111111")

    token = UserToken.objects.create(user=user)

    assert token.is_active is True
    assert token.expires_at > timezone.now()
    assert token.is_valid() is True
    assert str(token).startswith("Token(")

    # make it expired
    token.expires_at = timezone.now() - timedelta(days=1)
    token.save()
    assert token.is_valid() is False


@pytest.mark.django_db
def test_game_result_str_and_win_property():
    user = User.objects.create_user(username="gamer", phone_number="380222222222")

    result_win = GameResult.objects.create(user=user, number=444, result="win", prize=100)
    result_lose = GameResult.objects.create(user=user, number=333, result="lose", prize=0)

    assert result_win.win is True
    assert result_lose.win is False

    assert "win" in str(result_win)
    assert "lose" in str(result_lose)
