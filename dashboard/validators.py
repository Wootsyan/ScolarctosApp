from django.core.exceptions import ValidationError
from users.models import CustomUser

def validate_student_guardian(value):
    if CustomUser.objects.get(pk=value).user_type not in [CustomUser.STUDENT, CustomUser.GUARDIAN]:
        raise ValidationError(
            (f"Incorrect user type {value}"),
        )
