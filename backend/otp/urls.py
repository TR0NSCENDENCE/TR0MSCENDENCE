from django.urls import path, include
from .views import *

urlpatterns = [
    path('token/otp/<uuid:otp_uuid>/', OTPVerifyView.as_view(), name='verify-otp'),
]
