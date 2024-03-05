import os
from django.core.exceptions import ValidationError
    
class FileExtenstionValidator(object):
    def __init__(self, valid_extensions: list):
        self.valid_extensions = valid_extensions

    def __call__(self, value):
        if len(self.valid_extensions) > 0:
            extension = os.path.splitext(value.name)[1]
            if not extension.lower() in self.valid_extensions:
                raise ValidationError('Nieprawidłowe rozszerzenie pliku. Prawidłowe rozszerzenia: ' + ''.join(self.valid_extensions))