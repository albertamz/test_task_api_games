from rest_framework import serializers
from .models import GameResult


class GameResultSerializer(serializers.ModelSerializer):
    win = serializers.SerializerMethodField()
    prize = serializers.SerializerMethodField()

    @staticmethod
    def get_win(obj):
        return obj.win

    @staticmethod
    def get_prize(obj):
        return float(obj.prize)

    class Meta:
        model = GameResult
        fields = ['number', 'result', 'prize', 'played_at', 'win']
