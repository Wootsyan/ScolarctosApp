from django.db import models
from users.models import CustomUser as User
from files.models import File

class TeamTutor(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation = models.BooleanField(default=False)
    confirmation_file = models.ForeignKey(File, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Tutor: {self.tutor} | Confirmation status: {self.confirmation} | Confirmation file: {self.confirmation_file}'