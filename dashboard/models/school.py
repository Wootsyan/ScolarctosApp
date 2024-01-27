from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone
from users.models import CustomUser as User

class School(models.Model):
    FIRST_LEVEL = 1
    SECOND_LEVEL = 2

    SCHOOL_TYPE_CHOICES = (
        (FIRST_LEVEL, 'Podstawowa'),
        (SECOND_LEVEL, 'Ponadpodstawowa'),
    )

    name = models.CharField(max_length=255, unique=True)
    street = models.CharField(max_length=63)
    postcode = models.CharField(max_length=6, validators=[MinLengthValidator(6), RegexValidator(
                regex=r'^\d{2}-\d{3}$',
                message="Wprowadź prawidłowy kod pocztowy w formacie 12-345",
            ),])
    city = models.CharField(max_length=63)
    school_type = models.PositiveSmallIntegerField(choices=SCHOOL_TYPE_CHOICES, default=FIRST_LEVEL)
    accepted = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    added_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Name: {self.name} | Street: {self.street} | Postcode: {self.postcode} | City: {self.city} | Type: {self.school_type} | Accepted: {self.accepted} | Date: {self.added_date}'
    
    