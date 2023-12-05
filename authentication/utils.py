from django.conf import settings
from django.contrib.auth import get_user_model
import jwt
import datetime

def generate_token(user_id, user_email):
    payload_data = {
        "user_id": user_id,
        "user_email": user_email,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=settings.VERIFICATION_EXPIRE_MINUTES)
    }

    secret = settings.SECRET_KEY

    return jwt.encode(payload=payload_data, key=secret)


def check_token(user_id, token):
    secret = settings.SECRET_KEY
    try:
        decoded_token = jwt.decode(token, key=secret, algorithms=['HS256', ])
        if user_id == decoded_token['user_id']:
            user = get_user_model().objects.get(pk=user_id)
            if user.is_active:
                return {"status": False, "message": "ERROR: User is already active"}
            else:
                user.is_active = True
                user.save()
                return {"status": True, "message": "User has been activated"}
        else:
            return {"status": False, "message": "ERROR: Incorrect user"}
    except:
        return {"status": False, "message": "ERROR: Token expired or is incorrect"}