from django.db import models
from users.models import CustomUser as User
from files.models import File

class TeamGuardian(models.Model):
    guardian = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation = models.BooleanField(default=False)
    confirmation_file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'Guardian: {self.guardian} | Confirmation status: {self.confirmation} | Confirmation file: {self.confirmation_file}'