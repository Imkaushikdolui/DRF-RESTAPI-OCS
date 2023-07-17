from django.core.mail import send_mail
import random
from online_course_api.settings import EMAIL_HOST_USER
from .models import Account


def send_otp(email):
    subject = "TWO-FACTOR AUTHENTICATION"
    otp = random.randint(1000, 9999)
    message = f"VERIFY YOUR MAIL USING THIS OTP: {otp}"
    email_from = EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email], fail_silently=True)
    account_obj = Account.objects.get(email=email)
    account_obj.otp = otp
    account_obj.save()
