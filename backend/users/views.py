from django.shortcuts import render
from rest_framework import permissions, mixins, viewsets, generics, response, request, views, status, filters
from .serializers import *
from .models import User, UserProfile, FriendRequest
from .permissions import IsOwnerOrReadOnly
from otp.models import OTPInstance
from rest_framework import exceptions

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

class UserSendFriendRequestView(views.APIView):
    def post(self, request, pk, format=None):
        from_user = request.user
        try:
            to_user = User.objects.get(pk=pk)
        except:
            raise exceptions.NotFound(detail='User not found')
        if request.user.user_profile.friends.filter(pk=pk).exists():
            raise exceptions.APIException(detail='This user is already your friend')

        if from_user == to_user:
            raise exceptions.APIException(detail='You cant request you as friend')
        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            return response.Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.APIException(detail='Friend request was already send')

class UserAcceptFriendRequestView(views.APIView):
    def post(self, request, request_id, format=None):
        try:
            friend_request = FriendRequest.objects.get(id=request_id)
        except FriendRequest.DoesNotExist:
            raise exceptions.NotFound(detail='Friend request not found')
        if friend_request.to_user == request.user:
            friend_request.to_user.user_profile.friends.add(friend_request.from_user)
            friend_request.from_user.user_profile.friends.add(friend_request.to_user)
            friend_request.delete()
            return response.Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.PermissionDenied(detail='You are not the receiver of the friend request')

class UserRejectFriendRequestView(views.APIView):
    def delete(self, request, request_id, format=None):
        try:
            friend_request = FriendRequest.objects.get(id=request_id)
        except FriendRequest.DoesNotExist:
            raise exceptions.NotFound(detail='Friend request not found')
        if friend_request.to_user == request.user:
            friend_request.delete()
            return response.Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.PermissionDenied(detail='You are not the receiver of the friend request')

class UserRemoveFriendView(views.APIView):
    def delete(self, request, pk, format=None):
        try:
            friend = request.user.user_profile.friends.get(pk=pk)
            request.user.user_profile.friends.remove(friend)
            friend.user_profile.friends.remove(request.user)
        except User.DoesNotExist:
            raise exceptions.NotFound(detail='You cant remove friend if you are not friend...')
        return response.Response(status=200)
        # try:
        #     to_user = User.objects.get(pk=pk)
        # except:
        #     raise exceptions.NotFound(detail='User not found')
        # if from_user == to_user:
        #     raise exceptions.APIException(detail='You cant request you as friend')
        # friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        # if created:
        #     return response.Response(status=status.HTTP_200_OK)
        # else:
        #     raise exceptions.APIException(detail='Friend request was already send')

class UserReceivedFriendRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.all().filter(to_user=self.request.user)

class UserFriendListView(generics.ListAPIView):
    serializer_class = UserFriendSerializer

    def get_queryset(self):
        return self.request.user.user_profile.friends.all()
