from django.db import models
from django.utils import timezone
from users.models import CustomUser as User
from dashboard.validators import validate_student_guardian

class InvitationNoneAcceptedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(accepted__isnull=True)
    
class Invitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', validators=[validate_student_guardian])
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient', validators=[validate_student_guardian])
    accepted = models.BooleanField(blank=True, null=True, default=None) 
    created = models.DateField(default=timezone.now)

    objects = models.Manager()
    accepted_none_objects = InvitationNoneAcceptedManager()

    def __str__(self):
        return f'From: {self.sender.email} | To: {self.recipient.email} | Accepted: {self.accepted}'