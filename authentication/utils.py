from django.conf import settings
import jwt
import datetime
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.urls import reverse

def generate_token(user_id, user_email):
    payload_data = {
        "user_id": user_id,
        "user_email": user_email,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=settings.VERIFICATION_EXPIRE_MINUTES)
    }

    secret = settings.SECRET_KEY

    return jwt.encode(payload=payload_data, key=secret)


def check_token(token):
    secret = settings.SECRET_KEY
    try:
        decoded_token = jwt.decode(token, key=secret, algorithms=['HS256', ])
        return decoded_token
    except:
        return False
    
def send_verification_mail(to_user):
    email_verify_token = generate_token(to_user.id, to_user.email)
    email_data = {
        'user_name': to_user.first_name,
        'verification_time': settings.VERIFICATION_EXPIRE_MINUTES,
        'verification_url': settings.SITE_URL + reverse('verify_email', args=(to_user.id, email_verify_token))
    } 

    html_message = render_to_string(template_name="auth/email/email-confirmation.html", context=email_data)
    plain_message = strip_tags(html_message)
    try:
        mail = EmailMultiAlternatives(
            subject="Potwierdź swoje konto - Zespół Koala",
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_user.email],
        )
        mail.attach_alternative(html_message, "text/html")
        mail.send()
        return True
    except:
        return False