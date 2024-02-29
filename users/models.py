from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from gdpr.models import Gdpr

class CustomUser(AbstractBaseUser, PermissionsMixin):
    STUDENT = 1
    STUDENT_TEAM_MEMBER = 11
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
    phone_number = models.CharField(max_length=9, validators=[MinLengthValidator(9)], unique=True, null=True, default=None, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=STUDENT)
    gdpr = models.OneToOneField(Gdpr, null=True, blank=True, on_delete=models.CASCADE, related_name='gdpr')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        permissions = [
            ("add_admins", "Can add admins"),
            ("change_admins", "Can change admins"),
            ("delete_admins", "Can delete admins"),
            ("view_admins", "Can view admins"),
            ("add_organizers", "Can add organizers"),
            ("change_organizers", "Can change organizers"),
            ("delete_organizers", "Can delete organizers"),
            ("view_organizers", "Can view organizers"),
        ]

class CustomGroup():
    names = {
        CustomUser.STUDENT: "Students",
        CustomUser.GUARDIAN: "Guardians",
        CustomUser.ORGANIZER: "Organizers",
        CustomUser.ADMIN: "Admins",
    }