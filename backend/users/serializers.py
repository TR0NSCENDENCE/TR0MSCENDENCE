from rest_framework import serializers
from .models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(
        min_length=8,
        max_length=32
    )
    password = serializers.CharField(
        min_length=8,
        max_length=32,
        write_only=True
    )
    repassword = serializers.CharField(
        min_length=8,
        max_length=32,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'repassword']

    def validate_repassword(self, value):
        data = self.get_initial()  # Récupérer les données initiales
        password = data.get('password')

        if password != value:
            raise serializers.ValidationError("The passwords must match.")
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

    class Meta:
        model = User
        fields = ['email', 'username', 'user_profile', 'pk']
