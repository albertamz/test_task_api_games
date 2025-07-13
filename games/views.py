from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import HasValidToken
from .models import GameResult
from .services import GameLogic
from .serializers import GameResultSerializer


class TokenInfoView(APIView):
    permission_classes = [HasValidToken]

    def get(self, request, token):
        user = request.token_obj.user
        return Response({
            "user_id": user.id,
            "username": user.username,
            "phone_number": user.phone_number
        })


class TokenRenewView(APIView):
    permission_classes = [HasValidToken]

    def post(self, request, token):
        old_token = request.token_obj
        old_token.is_active = False
        old_token.save()

        new_token = old_token.__class__.objects.create(user=old_token.user)
        return Response({
            "new_token": new_token.token,
            "token_expires_at": new_token.expires_at
        })


class TokenDeactivateView(APIView):
    permission_classes = [HasValidToken]

    def post(self, request, token):
        request.token_obj.is_active = False
        request.token_obj.save()
        return Response({"message": "Token deactivated"})


class GamePlayView(APIView):
    permission_classes = [HasValidToken]
    serializer_class = GameResultSerializer

    def post(self, request, token):
        game_result = GameLogic.play(user=request.token_obj.user)
        serializer = self.serializer_class(game_result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GameHistoryView(APIView):
    permission_classes = [HasValidToken]
    serializer_class = GameResultSerializer

    def get(self, request, token):
        results = GameResult.objects.filter(user=request.token_obj.user).order_by('-played_at')[:3]
        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)
