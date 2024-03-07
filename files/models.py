import os
from django.db import models
from django.utils import timezone

from .utils import file_directory_path

class File(models.Model):
    path = models.FileField(upload_to=file_directory_path, max_length=254)
    name = models.CharField(max_length=255)
    added_date = models.DateTimeField(default=timezone.now)

    def delete(self, **kwargs):
        if self.path:
            if os.path.isfile(self.path.path):
                os.remove(self.path.path)
                
        super().delete(**kwargs)