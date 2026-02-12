from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.dtos.auth_response import UserAuthenticationService
from apps.users.dtos.verification_response import VerificationResponse
from apps.users.serializers import UserRegistrationSerializer, VerifyEmailSerializer, UserLoginSerializer
from apps.users.services.email_verification import VerificationService
from apps.users.services.registration import register_user, RegisterUserCommand
from apps.users.services.tokens import make_tokens


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

