import os
from django.db import models
from django.utils import timezone
from users.models import CustomUser as User
from dashboard.models.school import School
from dashboard.models.team_guardian import TeamGuardian
from files.models import File

class Team(models.Model):
    MAX_MEMBERS = 3
    MAX_FILES = 5

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
    files = models.ManyToManyField(
        File, 
        null=True, 
        blank=True, 
        related_name="teams",
    )
    added_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'Name: {self.name} | Desc: {self.description} | Leader: {self.leader} | Guardian: {self.team_guardian} | School: {self.school} | Date: {self.added_date}'
    
    def delete(self, **kwargs):
        self.team_members.all().delete()
        # Must delete each file separately
        if self.files.exists():
            first_file = self.files.first()
            files_dir = first_file.path.path
            files_dir = files_dir.replace(first_file.name, '')
            for file in self.files.all():
                file.delete()
            os.rmdir(files_dir)
        return super().delete(**kwargs)