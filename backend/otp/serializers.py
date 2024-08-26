from rest_framework import serializers
from .models import OTPInstance

class OTPSerializer(serializers.ModelSerializer):

    class Meta:
        model = OTPInstance
        fields = ['otp']
