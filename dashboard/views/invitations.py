from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView

from users.models import CustomUser
from dashboard.models import Team

'''
### Invitations Views
'''

@method_decorator(login_required, name='dispatch')
class InvitationsAvailableGuardiansListView(PermissionRequiredMixin, ListView):
    context_object_name = 'guardians'
    template_name = 'dashboard/invitations/available-guardians-list.html'

    def get_queryset(self):
        # Find all guardians connected to same school as user's team school
        # Guardian can connect with many teams
        leader_school = self.request.user.team_set.first().school
        return leader_school.guardians.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Opiekunowie z Twojej szkoły'
        return context
    
    def has_permission(self):
        leader = self.request.user
        if leader.user_type == CustomUser.STUDENT and leader.team_set.exists() and leader.team_set.first().team_guardian is None:
            return True
        return False
    
@method_decorator(login_required, name='dispatch')
class InvitationsAvailableTeamsListView(PermissionRequiredMixin, ListView):
    context_object_name = 'teams'
    template_name = 'dashboard/invitations/available-teams-list.html'

    def get_queryset(self):
        # Find all teams connected to same school as guardian's schools
        # Team can connect only one guardian
        guardian_schools = self.request.user.schools.all()
        return Team.objects.filter(school__in=guardian_schools, team_guardian__isnull=True, leader__isnull=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Zespoły z Twoich szkół'
        return context
    
    def has_permission(self):
        guardian = self.request.user
        if guardian.user_type == CustomUser.GUARDIAN and guardian.schools.exists():
            return True
        return False