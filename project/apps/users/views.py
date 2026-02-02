from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import UserRegistrationSerializer
from apps.users.services.registration import register_user, RegisterUserCommand


# Create your views here.
class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cmd = RegisterUserCommand(**serializer.validated_data) # **unpacks dictionary into arguments
        auth_response = register_user(cmd)

        return Response(auth_response.to_dict(), status=status.HTTP_201_CREATED)

