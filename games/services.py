import random
from .models import GameResult


class GameLogic:
    @staticmethod
    def play(user):
        number = random.randint(1, 1000)
        result = 'win' if number % 2 == 0 else 'lose'
        prize = 0

        if result == 'win':
            if number > 900:
                prize = number * 0.7
            elif number > 600:
                prize = number * 0.5
            elif number > 300:
                prize = number * 0.3
            else:
                prize = number * 0.1

        game_result = GameResult.objects.create(
            user=user,
            number=number,
            result=result,
            prize=round(prize, 2)
        )
        return game_result
