from django.shortcuts import render
from rest_framework import permissions, mixins, viewsets, generics, response, request, views, status, filters
from .serializers import *
from .models import User, UserProfile
from .permissions import IsOwnerOrReadOnly
from otp.models import OTPInstance

class UserRegistrationView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer
    search_fields = ['username']

class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = UserProfileUpdateSerializer
    lookup_field = 'user__pk'

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = UserSerializer
    lookup_field = 'pk'

class MyUserView(views.APIView):
    def get(self, request, format=None):
        return response.Response(UserSerializer(request.user).data)

class UserActivationView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, activation_uuid, format=None):
        try:
            user = User.objects.get(activation_uuid=activation_uuid)
        except User.DoesNotExist:
            return response.Response(status=404)
        user.is_active = True
        user.save()
        return response.Response(status=200)

def create_otp(user: User):
    return OTPInstance.objects.create(user=user)

class UserLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return response.Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED if 'non_field_errors' in serializer.errors.keys() else status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        otpinstance = create_otp(user)

        return response.Response({'otp_uuid': otpinstance.uuid}, status=200)

class MyUserPacmanDataView(views.APIView):
    def get(self, request, format=None):
        return response.Response(UserProfile.objects.get(user=request.user).pacman_data)
    def put(self, request, format=None):
        user_profile = request.user.user_profile
        user_profile.pacman_data = request.data
        user_profile.save()
        return response.Response(status=200)
