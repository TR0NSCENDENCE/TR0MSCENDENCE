from django.db import models
from users.models import User
from random import randint
from datetime import datetime, timedelta
from uuid import uuid4

def get_default_otp():
    otp = str(randint(1000, 9999))
    assert(len(otp == 6))
    return otp

def get_default_otp_expiry():
    return datetime.now() + timedelta(minutes=1)

class OTPInstance(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    otp = models.CharField(max_length=6, default=get_default_otp)
    otp_expiry = models.DateTimeField(blank=True, null=True, default=get_default_otp_expiry)
    max_otp_try = models.IntegerField(default=3)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
