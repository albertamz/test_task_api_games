from django.urls import path
from .views import TokenInfoView, TokenRenewView, TokenDeactivateView, GameHistoryView, GamePlayView

urlpatterns = [
    path('<uuid:token>', TokenInfoView.as_view(), name='game-token-info'),
    path('<uuid:token>/renew', TokenRenewView.as_view(), name='game-token-renew'),
    path('<uuid:token>/deactivate', TokenDeactivateView.as_view(), name='game-token-deactivate'),
    path('<uuid:token>/play', GamePlayView.as_view(), name='game-play'),
    path('<uuid:token>/history', GameHistoryView.as_view(), name='game-history'),
]
