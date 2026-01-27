from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.managers import UserManager


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