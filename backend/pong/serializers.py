from rest_framework import serializers
from .models import GameInstance
from users.serializers import UserSerializer

class GameInstanceInfoSerializer(serializers.ModelSerializer):
    player_one = UserSerializer()
    player_two = UserSerializer()

    class Meta:
        model = GameInstance
        exclude = ['id']
