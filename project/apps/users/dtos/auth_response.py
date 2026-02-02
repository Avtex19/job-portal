from dataclasses import dataclass

@dataclass(frozen=True)
class AuthResponse:
    user_id: int
    email: str
    role: str
    access_token: str
    refresh_token: str
    message: str = "Successful login"

    def to_dict(self):
        return {
            "message": self.message,
            "data": {
                "id": self.user_id,
                "email": self.email,
                "role": self.role,
            },
            "tokens": {
                "access": self.access_token,
                "refresh": self.refresh_token
            }
        }