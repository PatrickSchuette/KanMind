from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts_app.models import UserProfile

from .serializers import LoginSerializer, RegistrationSerializer


class RegistrationView(APIView):
    """Handles new user registration."""

    permission_classes = [AllowAny]
    
    def get_serializer(self, *args, **kwargs):
        """Provide a serializer instance so the browsable API can pre-fill the form."""
        return RegistrationSerializer(*args, **kwargs)

    def post(self, request):
        """Create a new user and return an auth token."""
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(self._build_response(token, user), status=status.HTTP_201_CREATED)

    def _build_response(self, token, user):
        """Build the response payload for a registered user."""
        return {
            'token': token.key,
            'fullname': user.profile.fullname,
            'email': user.email,
            'user_id': user.id,
        }


class LoginView(APIView):
    """Handles user login and token retrieval."""

    permission_classes = [AllowAny]
    
    def get_serializer(self, *args, **kwargs):
        """Provide a serializer instance so the browsable API can pre-fill the form."""
        return LoginSerializer(*args, **kwargs)

    def post(self, request):
        """Authenticate the user and return an auth token."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response(self._build_response(token, user), status=status.HTTP_200_OK)

    def _build_response(self, token, user):
        """Build the response payload for a logged-in user."""
        return {
            'token': token.key,
            'fullname': user.profile.fullname,
            'email': user.email,
            'user_id': user.id,
        }


class EmailCheckView(APIView):
    """Checks whether a given email is already registered."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return the user data for a given email, if it exists."""
        email = request.query_params.get('email')
        try:
            profile = UserProfile.objects.select_related(
                'user').get(user__email=email)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self._build_response(profile), status=status.HTTP_200_OK)

    def _build_response(self, profile):
        """Build the response payload for the found user."""
        return {
            'id': profile.user.id,
            'email': profile.user.email,
            'fullname': profile.fullname,
        }


class LogoutView(APIView):
    """Handles user logout by deleting the current auth token."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Delete the requesting user's auth token."""
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
