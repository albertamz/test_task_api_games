import pytest
from games.services import GameLogic
from users.models import User
from games.models import GameResult


@pytest.mark.django_db
def test_game_logic_play_creates_result():
    user = User.objects.create_user(username="testuser", phone_number="1234567890")

    result = GameLogic.play(user=user)

    assert isinstance(result, GameResult)
    assert result.user == user
    assert 1 <= result.number <= 1000
    assert result.result in ['win', 'lose']
    assert result.prize >= 0

    if result.result == 'win':
        if result.number > 900:
            expected = result.number * 0.7
        elif result.number > 600:
            expected = result.number * 0.5
        elif result.number > 300:
            expected = result.number * 0.3
        else:
            expected = result.number * 0.1
        assert abs(result.prize - expected) < 0.01
    else:
        assert result.prize == 0
