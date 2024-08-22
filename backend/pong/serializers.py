from rest_framework import serializers
from .models import GameInstance, TournamentInstance
from users.serializers import UserSerializer

class GameInstanceInfoSerializer(serializers.ModelSerializer):
    player_one = UserSerializer()
    player_two = UserSerializer()
    tournament_uuid = serializers.UUIDField()

    class Meta:
        model = GameInstance
        exclude = ['id']

class TournamentInstanceInfoSerializer(serializers.ModelSerializer):
    gameinstance_half_1 = GameInstanceInfoSerializer()
    gameinstance_half_2 = GameInstanceInfoSerializer()
    gameinstance_final = GameInstanceInfoSerializer()

    class Meta:
        model = TournamentInstance
        exclude = ['id']
