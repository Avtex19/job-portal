from dataclasses import dataclass

from django.contrib.auth import get_user_model

from apps.users.dtos.auth_response import AuthResponse
from apps.users.services.tokens import make_tokens

User = get_user_model()

@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    password: str
    first_name: str
    last_name: str
    role: str


def register_user(cmd:RegisterUserCommand) -> AuthResponse:
    user = User.objects.create_user(
        email=cmd.email,
        password=cmd.password,
        first_name=cmd.first_name,
        last_name=cmd.last_name,
        role=cmd.role
    )

    tokens = make_tokens(user)

    return AuthResponse(
        user_id=user.id,
        email=user.email,
        role=user.role,
        access_token=tokens["access"],
        refresh_token=tokens["refresh"],
        message="Successful registration")




