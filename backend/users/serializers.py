from rest_framework import serializers
from .models import User, UserProfile
from django.core.files.uploadedfile import InMemoryUploadedFile
from uuid import uuid4
import django.contrib.auth.password_validation as validators

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['get_thumbnail']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField()

    class Meta:
        model = UserProfile
        fields = ['profile_picture']

    def validate_profile_picture(self, value: InMemoryUploadedFile):
        value.name = str(uuid4())+'.jpg'
        return value

    def update(self, instance, validated_data):
        instance.thumbnail = None
        instance.profile_picture = validated_data['profile_picture']
        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    repassword = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'repassword']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_repassword(self, value):
        data = self.get_initial()  # Récupérer les données initiales
        password = data.get('password')

        if password != value:
            raise serializers.ValidationError("The passwords must match.")
        return value

    def validate_password(self, value):
        try:
            validators.validate_password(value)
        except validators.ValidationError as e:
            raise serializers.ValidationError(e.messages[0])
        return value


    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    # Used in LoaderboardListView
    num_wins = serializers.IntegerField(required=False, read_only=True)
    num_played = serializers.IntegerField(required=False, read_only=True)
    win_rate = serializers.FloatField(required=False, read_only=True)
    rank = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'user_profile', 'pk', 'num_wins', 'num_played', 'win_rate', 'rank']
        read_only_fields = ['user_profile', 'pk']
