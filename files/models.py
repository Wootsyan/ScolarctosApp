from django.db import models
from django.conf import settings
from django.utils import timezone

class File(models.Model):
    path = models.FileField(upload_to=settings.STATIC_DOCUMENTS_DIR, max_length=254)
    name = models.CharField(max_length=255)
    added_date = models.DateTimeField(default=timezone.now)