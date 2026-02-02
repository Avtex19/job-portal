# apps/users/serializers.py
from rest_framework import serializers

from apps.users.models import User


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    role = serializers.ChoiceField(choices=["CANDIDATE", "EMPLOYER"])

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value.lower().strip()



