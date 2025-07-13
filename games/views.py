from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import UserToken
from .models import GameResult
from .services import GameLogic
from .serializers import GameResultSerializer


def get_token_or_error(token_string):
    try:
        token_obj = UserToken.objects.get(token=token_string)
        if not token_obj.is_valid():
            return None, Response({"error": "Token is expired or inactive"}, status=status.HTTP_403_FORBIDDEN)
        return token_obj, None
    except UserToken.DoesNotExist:
        return None, Response({"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)


class TokenInfoView(APIView):
    def get(self, request, token):
        token_obj, error_response = get_token_or_error(token)
        if error_response:
            return error_response

        user = token_obj.user
        return Response({
            "user_id": user.id,
            "username": user.username,
            "phone_number": user.phone_number
        })


class TokenRenewView(APIView):
    def post(self, request, token):
        token_obj, error_response = get_token_or_error(token)
        if error_response:
            return error_response

        # Деактивировать старый токен
        token_obj.is_active = False
        token_obj.save()

        # Создать новый токен
        new_token = UserToken.objects.create(user=token_obj.user)
        return Response({
            "new_token": new_token.token,
            "token_expires_at": new_token.expires_at
        })


class TokenDeactivateView(APIView):
    def post(self, request, token):
        try:
            token_obj = UserToken.objects.get(token=token)
        except UserToken.DoesNotExist:
            return Response({"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)

        token_obj.is_active = False
        token_obj.save()

        return Response({"message": "Token deactivated"}, status=status.HTTP_200_OK)


class GamePlayView(APIView):
    def post(self, request, token):
        token_obj, error_response = get_token_or_error(token)
        if error_response:
            return error_response

        game_result = GameLogic.play(user=token_obj.user)
        serializer = GameResultSerializer(game_result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GameHistoryView(APIView):
    def get(self, request, token):
        token_obj, error_response = get_token_or_error(token)
        if error_response:
            return error_response

        results = GameResult.objects.filter(user=token_obj.user).order_by('-played_at')[:3]
        serializer = GameResultSerializer(results, many=True)
        return Response(serializer.data)
