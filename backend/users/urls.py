from django.urls import path, include
from .views import *

urlpatterns = [
    path('me/', MyUserView.as_view(), name='me-detail'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('user/<int:pk>/', UserView.as_view(), name='user-detail'),
    path('user/<int:user__pk>/update/', UserUpdateView.as_view(), name='user-update'),
]
