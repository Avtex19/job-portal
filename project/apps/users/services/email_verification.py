import datetime
import secrets
import hashlib
from django.conf import settings
from django.utils import timezone
from django.db import transaction  # Important for data integrity
from ..models import EmailVerification


def _generate_token_payload():
    """Internal helper to keep the logic encapsulated."""
    raw = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256((raw + settings.SECRET_KEY).encode()).hexdigest()
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