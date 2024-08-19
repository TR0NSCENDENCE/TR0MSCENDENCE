from django.urls import path, include
from .views import *

urlpatterns = [
    path('gameinstance/<uuid:uuid>/', GameInstanceRetrieveView.as_view(), name='gameinstance-detail'),
    path('user/<int:pk>/matchs/', UserGameListView.as_view(), name='list-user-matchs'),
    path('user/<int:pk>/winned/', UserGameWinnedCount.as_view(), name='winned-count'),
    path('user/<int:pk>/losed/', UserGameLosedCount.as_view(), name='losed-count'),
]
