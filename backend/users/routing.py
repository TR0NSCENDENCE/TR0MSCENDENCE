from django.urls import path
from .views import *
from .consumers import OnlineTracker

ws_urlpatterns = [
    path('api/ws/onlinetracker/', OnlineTracker.as_asgi()),
]
