from django.urls import path, include
from .views import *

urlpatterns = [
    path('gameinstance/<uuid:uuid>/', GameInstanceRetrieveView.as_view(), name='gameinstance-detail'),
]
