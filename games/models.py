from django.db import models
from users.models import User


class GameResult(models.Model):
    RESULT_CHOICES = [
        ('win', 'Win'),
        ('lose', 'Lose'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_results')
    number = models.IntegerField()
    result = models.CharField(max_length=4, choices=RESULT_CHOICES)
    prize = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    played_at = models.DateTimeField(auto_now_add=True)

    @property
    def win(self):
        return self.result == 'win'

    def __str__(self):
        return f"{self.user.username}: {self.result} ({self.number})"
