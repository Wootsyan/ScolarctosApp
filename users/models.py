from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    STUDENT = 1
    GUARDIAN = 2
    ORGANIZER = 3
    ADMIN = 4

    USER_TYPE_CHOICES = (
        (STUDENT, 'Uczeń'),
        (GUARDIAN, 'Opiekun'),
        (ORGANIZER, 'Organizator'),
        (ADMIN, 'Administrator'),
    )

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=9, validators=[MinLengthValidator], unique=True, null=True, default=None)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    data_joined = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=STUDENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")