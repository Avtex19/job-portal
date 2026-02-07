from django.conf import settings
from django.core.mail import send_mail
class EmailService:
    @staticmethod
    def send_verification_email(user,token:str):
        verification_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"

        subject = "Verify your email"
        message = f"Click here to verify: {verification_link}"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
