from dataclasses import dataclass
from django.contrib.auth import get_user_model
from django.db import transaction

from apps.users.dtos.auth_response import AuthResponse
from apps.users.services.email import EmailService
from apps.users.services.email_verification import VerificationService

User = get_user_model()
@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    password: str
    first_name: str
    last_name: str
    role: str

def register_user(cmd: RegisterUserCommand) -> AuthResponse:
    with transaction.atomic():
        user = User.objects.create_user(
            email=cmd.email,
            password=cmd.password,
            first_name=cmd.first_name,
            last_name=cmd.last_name,
            role=cmd.role,
            is_active=False,
        )

        # If this fails, the User creation above is "rolled back" (undone)
        raw_token = VerificationService.create_verification(user)

        # Send Email
        transaction.on_commit(
            lambda: EmailService.send_verification_email(user, raw_token)
        )

    return AuthResponse(
        user_id=user.id,
        email=user.email,
        role=user.role,
        message="Successful registration"
    )


