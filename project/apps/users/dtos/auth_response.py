from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime
from django.utils import timezone

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


@dataclass(frozen=True)
class AuthResponse:
    user_id: int
    email: str
    role: str
    message: str = "Successful login"

    def to_dict(self):
        return {
            "message": self.message,
            "data": {
                "id": self.user_id,
                "email": self.email,
                "role": self.role,
            },
        }

@dataclass(frozen=True)
class LoginMessage:
    user: Optional[User] = None
    error: Optional[str] = None

    def is_success(self):
        return self.user is not None and self.error is None
@dataclass(frozen=True)
class LoginResponse:
    user_id: int
    email: str
    role: str
    first_name: str
    last_name: str

    last_login: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class UserAuthenticationService:

    @staticmethod
    def authenticate_user(email: str, password: str) ->LoginMessage:
        if not email or not password:
            return LoginMessage(error="Invalid email or password")

        user = authenticate(email=email, password=password)
        if not user:
            return LoginMessage(error="Invalid email or password")
        if not user.is_active:
            return LoginMessage(error="User account is disabled")

        return LoginMessage(user=user)

    @staticmethod
    def update_last_login(user: User) -> None:
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])


