from django.urls import path
from .views import *
from .consumers import GameConsumer, MatchmakingConsumer, TournamentConsumer

ws_urlpatterns = [
    path('api/ws/gameinstance/<uuid:instance_uuid>/', GameConsumer.as_asgi()),
    path('api/ws/tournamentinstance/<uuid:instance_uuid>/', TournamentConsumer.as_asgi()),
    path('api/ws/matchmaking/<str:match_type>/', MatchmakingConsumer.as_asgi()),
]
