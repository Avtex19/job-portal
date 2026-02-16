from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.dtos.auth_response import UserAuthenticationService
from apps.users.dtos.verification_response import VerificationResponse
from apps.users.serializers import UserRegistrationSerializer, VerifyEmailSerializer, UserLoginSerializer, \
    LogoutSerializer
from apps.users.services.blacklist import DenyBlacklistedToken
from apps.users.services.email_verification import VerificationService
from apps.users.services.registration import register_user, RegisterUserCommand
from apps.users.services.tokens import make_tokens
from .services.logout import logout_refresh_token


# Create your views here.
class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cmd = RegisterUserCommand(**serializer.validated_data) # **unpacks dictionary into arguments
        auth_response = register_user(cmd)

        return Response(auth_response.to_dict(), status=status.HTTP_201_CREATED)

class VerifyEmailAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']

        try:
            tokens = VerificationService.verify_token_and_issue_jwt(token)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        response_data = VerificationResponse.from_jwt_dict(tokens)

        return Response(response_data.to_dict(), status=status.HTTP_200_OK)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = UserAuthenticationService.authenticate_user(
            email = serializer.validated_data['email'],
            password = serializer.validated_data['password']
        )

        if not result.is_success():
            return Response(
                {"detail": result.error},
                status=status.HTTP_401_UNAUTHORIZED
            )
        tokens = make_tokens(result.user)
        return Response({
            "message": "Login successful",
            "user": {
                "id": result.user.id,
                "email": result.user.email,
                "role": result.user.role,
            },
            "tokens": tokens
        }, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError  # <-- Import this!

from .serializers import LogoutSerializer


class LogoutAPIView(APIView):
    # Your permission classes are perfect!
    permission_classes = (IsAuthenticated, DenyBlacklistedToken)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            logout_refresh_token(serializer.validated_data['refresh'])

            # FIX 1: Send a success response back to the user!
            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_200_OK
            )

        # FIX 2: Catch TokenError instead of KeyError
        except TokenError:
            return Response(
                {"detail": "Token is invalid or has already been blacklisted."},
                status=status.HTTP_400_BAD_REQUEST
            )





