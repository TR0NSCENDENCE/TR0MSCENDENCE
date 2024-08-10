from django.urls import path, include
from .views import *

urlpatterns = [
    path('me/', MyUserProfileView.as_view(), name='me-detail'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('userprofile/<int:user__pk>/', UserProfileView.as_view(), name='userprofile-detail-update'),
]
