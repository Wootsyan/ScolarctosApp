from django.db import models

class School(models.Model):
    FIRST_LEVEL = 1
    SECOND_LEVEL = 2

    SCHOOL_TYPE_CHOICES = (
        (FIRST_LEVEL, 'Podstawowa'),
        (SECOND_LEVEL, 'Ponadpodstawowa'),
    )

    'name
    'street
    'postcode
    'city
    'school_type
    'accepted
    'added_by