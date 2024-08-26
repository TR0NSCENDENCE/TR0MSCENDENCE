from django.urls import path, include
from .views import *

urlpatterns = [
    path('gameinstance/<uuid:uuid>/', GameInstanceRetrieveView.as_view(), name='gameinstance-detail'),
    path('tournamentinstance/<uuid:uuid>/', TournamentInstanceRetrieveView.as_view(), name='tournamentinstance-detail'),
    path('user/<int:pk>/matchs/', UserGameListView.as_view(), name='list-user-matchs'),
    path('user/<int:pk>/tournaments/', UserTournamentListView.as_view(), name='list-user-tournaments'),
    path('user/<int:pk>/winned/', UserGameWinnedCount.as_view(), name='winned-count'),
    path('leaderboard/', LeaderboardListView.as_view(), name='leaderboard'),
    path('user/<int:pk>/losed/', UserGameLosedCount.as_view(), name='losed-count'),
]
