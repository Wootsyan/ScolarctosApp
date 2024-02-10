from django.db import models
from django.utils import timezone
from users.models import CustomUser as User
from dashboard.models.school import School
from dashboard.models.team_guardian import TeamGuardian

class Team(models.Model):
    name = models.CharField(max_length=63, unique=True)
    description = models.TextField(blank=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    team_guardian = models.ForeignKey(TeamGuardian, on_delete=models.CASCADE, null=True, blank=True)
    team_members = models.ManyToManyField(
        User, 
        null=True, 
        blank=True, 
        related_name="team_members", 
        related_query_name="team_member",
        )
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    editable = models.BooleanField(default=True)
    added_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'Name: {self.name} | Desc: {self.description} | Leader: {self.leader} | Guardian: {self.team_guardian} | School: {self.school} | Date: {self.added_date}'