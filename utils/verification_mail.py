from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user_email, otp):
    """Send an email with an OTP for email verification."""
    subject = "Email Verification"
    message = (
        f"Your OTP for email verification is {otp}.\n"
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
