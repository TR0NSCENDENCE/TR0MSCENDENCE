from django.shortcuts import render
from django.db.models import Q, Count, F, ExpressionWrapper, FloatField, functions, expressions, Case, When, IntegerField
from users.models import User
from django.http import Http404
import json
from rest_framework import permissions, mixins, viewsets, generics, response, request, views, status
from .serializers import *
from .models import GameInstance, TournamentInstance

def get_user_rank():
    return User.objects.filter(Q(gameinstance_player_one__state='FD')|Q(gameinstance_player_two__state='FD')).annotate(
            num_wins=Count('gameinstance_winner', filter=Q(gameinstance_winner__state='FD'), distinct=True),
            num_played=Count('gameinstance_player_one', filter=Q(gameinstance_player_one__state='FD'), distinct=True) + Count('gameinstance_player_two', filter=Q(gameinstance_player_two__state='FD'), distinct=True,)
            ).annotate(
                win_rate=ExpressionWrapper((F('num_wins') * 1.0 / F('num_played')) * 100, output_field=FloatField())
            ).annotate(
                rank=expressions.Window(
                expression=functions.RowNumber(),
                order_by=('-num_wins',))
            )

class GameInstanceRetrieveView(generics.RetrieveAPIView):
    queryset = GameInstance.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uuid'
    serializer_class = GameInstanceInfoSerializer

class TournamentInstanceRetrieveView(generics.RetrieveAPIView):
    queryset = TournamentInstance.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uuid'
    serializer_class = TournamentInstanceInfoSerializer

class UserTournamentListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TournamentInstanceInfoSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return TournamentInstance.objects.filter(Q(player_one__pk=pk) \
                                                | Q(player_two__pk=pk) \
                                                | Q(player_thr__pk=pk) \
                                                | Q(player_fou__pk=pk) \
                                            ).filter(state='FD').order_by('-finished_at')

class UserGameListView(generics.ListAPIView):
    serializer_class = GameInstanceInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return GameInstance.objects.filter(Q(player_one__pk=pk) | Q(player_two__pk=pk)).filter(state='FD').order_by('-finished_at')

class LeaderboardListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return get_user_rank().order_by('rank')

class UserGameWinnedCount(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        pk = kwargs['pk']
        if not User.objects.filter(pk=pk).exists():
            raise Http404
        winned = GameInstance.objects.filter(Q(player_one__pk=pk) | Q(player_two__pk=pk)).filter(Q(winner=pk)).filter(state='FD').count()
        return response.Response({'winned_count': winned})

class UserGameLosedCount(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        pk = kwargs['pk']
        if not User.objects.filter(pk=pk).exists():
            raise Http404
        losed = GameInstance.objects.filter(Q(player_one__pk=pk) | Q(player_two__pk=pk)).exclude(Q(winner=pk)).filter(state='FD').count()
        return response.Response({'losed_count': losed})