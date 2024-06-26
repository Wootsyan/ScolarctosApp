from django.db import models

from files.models import File

class Gdpr(models.Model):
    gdpr_consent = models.BooleanField(default=False)
    parental_consent = models.BooleanField(default=False)

    def __str__(self):
        return f'gdpr: {self.gdpr_consent} | parental_consent: {self.parental_consent}'
