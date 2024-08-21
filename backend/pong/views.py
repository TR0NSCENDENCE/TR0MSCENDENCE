from django.shortcuts import render
from django.db.models import Q
from users.models import User
from django.http import Http404
import json
from rest_framework import permissions, mixins, viewsets, generics, response, request, views, status
from .serializers import *
from .models import GameInstance, TournamentInstance

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

class UserGameListView(generics.ListAPIView):
    serializer_class = GameInstanceInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return GameInstance.objects.filter(Q(player_one__pk=pk) | Q(player_two__pk=pk)).filter(state='FD')

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