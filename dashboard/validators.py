from django.core.exceptions import ValidationError
from users.models import CustomUser

def validate_student_guardian(value):
    if value not in [CustomUser.STUDENT, CustomUser.GUARDIAN]:
        raise ValidationError(
            ("Incorrect user type"),
        )
