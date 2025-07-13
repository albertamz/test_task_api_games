from rest_framework import serializers
from .models import GameResult


class GameResultSerializer(serializers.ModelSerializer):
    prize = serializers.SerializerMethodField()
    random_number = serializers.IntegerField(source='number', read_only=True)

    @staticmethod
    def get_prize(obj):
        return float(obj.prize)

    class Meta:
        model = GameResult
        fields = ['random_number', 'result', 'prize']
