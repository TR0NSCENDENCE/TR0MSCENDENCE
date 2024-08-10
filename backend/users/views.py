from django.shortcuts import render
from rest_framework import permissions, mixins, viewsets, generics, response, request, views, status
from .serializers import *
from .models import User, UserProfile
from .permissions import IsOwnerOrReadOnly

class UserRegistrationView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveAPIView,
                    generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'user__pk'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserProfileUpdateSerializer
        return UserProfileSerializer

class MyUserProfileView(views.APIView):
    def get(self, request, format=None):
        return response.Response(UserProfileSerializer(request.user.user_profile).data)
