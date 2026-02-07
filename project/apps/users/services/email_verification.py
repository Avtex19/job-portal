import datetime
import secrets
import hashlib
from django.conf import settings
from django.utils import timezone
from django.db import transaction  # Important for data integrity

from .tokens import make_tokens
from ..models import EmailVerification

def _hash_raw_token(raw_token: str) -> str:
    """The single source of truth for hashing tokens."""
    return hashlib.sha256((raw_token + settings.SECRET_KEY).encode()).hexdigest()
def _generate_token_payload():
    """Internal helper to keep the logic encapsulated."""
    raw = secrets.token_urlsafe(32)
    token_hash = _hash_raw_token(raw)
    return raw, token_hash


class VerificationService:
    @staticmethod
    def create_verification(user) -> str:
        # Wrap in a transaction so if the save fails, the old tokens aren't lost
        with transaction.atomic():
            # 1. Invalidate any existing unused tokens for this user
            # This ensures only the NEW token sent to their email will work
            EmailVerification.objects.filter(
                user=user,
                used_at__isnull=True
            ).delete()

            # 2. Generate new credentials
            raw_token, token_hash = _generate_token_payload()


            # 3. Save to DB
            EmailVerification.objects.create(
                user=user,
                token_hash=token_hash,
                expires_at=timezone.now() + datetime.timedelta(hours=24)
            )

        return raw_token

    @staticmethod
    def verify_token_and_issue_jwt(raw_token:str) -> dict:
        token_hash = _hash_raw_token(raw_token)

        # Grab the token and user in one go, then lock the row so nobody else can double-click/reuse it.
        with transaction.atomic():
            verification = (
                EmailVerification.objects.select_related("user").select_for_update().filter(
                    token_hash=token_hash,
                    used_at__isnull=True,
                    expires_at__gt = timezone.now()
                ).first()
            )

            if not verification:
                raise ValueError('No verification token')

            user = verification.user
            if not user.is_active:
                user.is_active = True
                user.save(update_fields=['is_active'])

            verification.used_at = timezone.now()
            verification.save(update_fields=['used_at'])

            return make_tokens(user)


