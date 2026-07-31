from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from accounts_app.models import UserProfile


class RegistrationSerializer(serializers.Serializer):
    """Validates registration data and creates a new user with a profile."""

    fullname = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        """Ensure the email is not already registered."""
        email_already_taken = User.objects.filter(email=value).exists()
        if email_already_taken:
            raise serializers.ValidationError(f'Email "{value}" is already in use.')
        return value

    def validate(self, attrs):
        """Ensure both passwords match."""
        passwords_match = attrs['password'] == attrs['repeated_password']
        if not passwords_match:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs

    def create(self, validated_data):
        """Create the User and the linked UserProfile."""
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        UserProfile.objects.create(
            user=user,
            fullname=validated_data['fullname'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Validates login credentials and authenticates the user."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Authenticate the user and attach it to the validated data."""
        user = authenticate(
            username=attrs['email'],
            password=attrs['password'],
        )
        if user is None:
            raise serializers.ValidationError('Invalid email or password.')
        attrs['user'] = user
        return attrs
