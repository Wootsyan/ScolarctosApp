import string
from django.conf import settings
from django.utils.crypto import get_random_string

def generate_team_member_email(first_name: str, last_name: str, team_name: str) -> str:
    email = f"{first_name}.{last_name}.{team_name}.{get_random_string(length=3, allowed_chars=string.digits)}@{settings.SITE_DOMAIN}"
    email = email.lower().replace(' ', '_')
    return email
