from rest_framework_simplejwt.tokens import RefreshToken

def logout_refresh_token(refresh: str) -> None:
    token = RefreshToken(refresh)
    token.blacklist()