from django.urls import path, include
from .views import *

urlpatterns = [
    path('me/', MyUserView.as_view(), name='me-detail'),
    path('me/pacman-data/', MyUserPacmanDataView.as_view(), name='me-pacman-data'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('user/<int:pk>/', UserView.as_view(), name='user-detail'),
    path('user/<int:pk>/send-request/', UserSendFriendRequestView.as_view(), name='user-request'),
    path('user/<int:pk>/remove-friend/', UserRemoveFriendView.as_view(), name='user-remove-friend'),
    path('user/<int:pk>/update-cred/', UserUpdateView.as_view(), name='user-update-cred'),
    path('friend-request/<int:request_id>/accept/', UserAcceptFriendRequestView.as_view(), name='accept-request'),
    path('friend-request/<int:request_id>/reject/', UserRejectFriendRequestView.as_view(), name='reject-request'),
    path('user/friend-request-received/', UserReceivedFriendRequestListView.as_view(), name='list-request'),
    path('user/friend-list/', UserFriendListView.as_view(), name='friend-list'),
    path('user/<int:user__pk>/update/', UserProfileUpdateView.as_view(), name='user-update'),
    path('user/search/', UserListView.as_view(), name='user-search'),
    path('activation/<uuid:activation_uuid>/', UserActivationView.as_view(), name='account-activation'),
    path('login/', UserLoginView.as_view(), name='login'),
]
