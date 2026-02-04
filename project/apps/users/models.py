from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.managers import UserManager
from config import settings


# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CANDIDATE = 'CANDIDATE', 'Candidate'
        EMPLOYER = 'EMPLOYER', 'Employer'


    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CANDIDATE,
    blank=False,
    null=False,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()


class EmailVerification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verifications",
    )

    # Store hash, not raw token
    token_hash = models.CharField(max_length=128, unique=True)

    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)

    last_sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "expires_at"]),
            models.Index(fields=["used_at", "expires_at"]),
        ]

    def __str__(self):
        return f"EmailVerification(user_id={self.user_id}, used={self.used_at is not None})"
