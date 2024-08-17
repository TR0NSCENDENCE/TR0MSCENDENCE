from django.shortcuts import render
from rest_framework import permissions, mixins, viewsets, generics, response, request, views, status
from .serializers import *
from .models import GameInstance

class GameInstanceRetrieveView(generics.RetrieveAPIView):
    queryset = GameInstance.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uuid'
    serializer_class = GameInstanceInfoSerializer
