from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView, SingleObjectMixin

from dashboard.utils import generate_team_member_email
from dashboard.models import Team
from dashboard.forms import CreateTeamForm, CreateTeamMemberForm, UpdateTeamMemberForm, UpdateTeamLeaderForm, ConnectTeamLeaderForm
from users.models import CustomUser
from gdpr.models import Gdpr

'''
### Teams Views
'''

@method_decorator(login_required, name='dispatch')
class TeamsListView(PermissionRequiredMixin, ListView):
    model = Team
    context_object_name = 'teams'
    template_name = 'dashboard/teams/list.html'
    permission_required = ('dashboard.view_team')

    def get_context_data(self, **kwargs):
        context = super(TeamsListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Zespoły'
        return context
    
@method_decorator(login_required, name='dispatch')
class TeamsDetailView(PermissionRequiredMixin, DetailView):
    model = Team
    context_object_name = 'team'
    template_name = 'dashboard/teams/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TeamsDetailView, self).get_context_data(**kwargs)
        context['page_name'] = f"{context['team'].name}"
        return context
    
    def has_permission(self):
        if self.get_object() == Team.objects.filter(leader=self.request.user).first():
            return True
        else:
            return self.request.user.has_perm('dashboard.view_team')

@method_decorator(login_required, name='dispatch')
class TeamsCreateView(PermissionRequiredMixin, CreateView):
    model = Team
    template_name = 'dashboard/teams/add.html'
    form_class = CreateTeamForm

    def get_context_data(self, **kwargs):
        context = super(TeamsCreateView, self).get_context_data(**kwargs)
        context['page_name'] = "Utwórz zespół"
        return context
    
    def form_valid(self, form):
        self.object = form.save() 
        self.object.editable = True
        if self.request.user.user_type == CustomUser.STUDENT:
            self.object.leader = self.request.user
            user_gdpr = Gdpr.objects.create()
            user_gdpr.save()
            self.request.user.gdpr = user_gdpr
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        kwargs = {'pk': self.object.id}
        if '_save' in self.request.POST:
            return reverse_lazy('dashboard:teams-detail', kwargs=kwargs)
        elif '_continue' in self.request.POST:
            return reverse_lazy('dashboard:teams-edit', kwargs=kwargs)
    
    def has_permission(self):
        if Team.objects.filter(leader=self.request.user):
            return False
        else:
            return self.request.user.has_perm('dashboard.add_team')
        
        
@method_decorator(login_required, name='dispatch')
class TeamsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Team
    context_object_name = 'team'
    template_name = 'dashboard/teams/edit.html'
    form_class = CreateTeamForm

    def get_context_data(self, **kwargs):
        context = super(TeamsUpdateView, self).get_context_data(**kwargs)
        context['page_name'] = f"Edycja: {context['team'].name}"
        return context

    def has_permission(self):
        self.object = self.get_object()
        if self.request.user == self.object.leader and self.object.editable:
            return True
        else:
            return self.request.user.has_perm('dashboard.change_team')
        
    def form_valid(self, form):
        self.object = form.save()
        if self.request.user == self.object.leader:
            self.object.editable = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        self.object = self.get_object()
        kwargs = {'pk': self.object.id}
        if '_save' in self.request.POST:
            return reverse_lazy('dashboard:teams-detail', kwargs=kwargs)
        elif '_continue' in self.request.POST:
            return reverse_lazy('dashboard:teams-edit', kwargs=kwargs)
        

@method_decorator(login_required, name='dispatch')
class TeamsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Team
    context_object_name = 'team'
    template_name = 'dashboard/teams/delete.html'

    def get_context_data(self, **kwargs):
        context = super(TeamsDeleteView, self).get_context_data(**kwargs)
        context['page_name'] = f"Zespół: {context['team'].name}"
        return context
    
    def has_permission(self):
        self.object = self.get_object()
        if self.request.user == self.object.leader and self.object.editable:
            return True
        else:
            return self.request.user.has_perm('dashboard.delete_team')
        
    def get_success_url(self):
        self.object = self.get_object()
        if self.request.user == self.object.leader:
            return reverse_lazy('dashboard:index')
        else:
            return reverse_lazy('dashboard:teams-list')
        
@method_decorator(login_required, name='dispatch')
class TeamsMembersCreateView(PermissionRequiredMixin, SingleObjectMixin, FormView):
    model = Team
    context_object_name = 'team'
    template_name = 'dashboard/teams/members/add.html'
    form_class = CreateTeamMemberForm

    def get_context_data(self, **kwargs):
        context = super(TeamsMembersCreateView, self).get_context_data(**kwargs)
        context['page_name'] = "Dodaj członka zespołu"
        return context
    
    def has_permission(self):
        self.object = self.get_object()
        if self.request.user == self.object.leader and self.object.editable:
            return True
        else:
            return self.request.user.has_perm('dashboard.change_team')
        
    def form_valid(self, form):
        team_member = form.save()
        self.team = self.get_object()
        team_member.email = generate_team_member_email(team_member.first_name, team_member.last_name, self.team.name)
        team_member.user_type = CustomUser.STUDENT_TEAM_MEMBER
        team_member_gdpr = Gdpr.objects.create(gdpr_consent=form.cleaned_data['gdpr_consent'], parental_consent=form.cleaned_data['parental_consent'])
        team_member_gdpr.save()
        team_member.gdpr = team_member_gdpr
        team_member.save()
        self.team.team_members.add(team_member)
        self.team.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        self.team = self.get_object()
        kwargs = {'pk': self.team.id}
        return reverse_lazy('dashboard:teams-detail', kwargs=kwargs)
    
@method_decorator(login_required, name='dispatch')
class TeamsMembersUpdateView(PermissionRequiredMixin, UpdateView):
    model = CustomUser
    context_object_name = 'team_member'
    template_name = 'dashboard/teams/members/edit.html'
    form_class = UpdateTeamMemberForm

    def get_context_data(self, **kwargs):
        context = super(TeamsMembersUpdateView, self).get_context_data(**kwargs)
        context['page_name'] = f"Edytuj członka zespołu: {context['team_member'].first_name} {context['team_member'].last_name}"
        context['team'] = self.get_object().team_members.first()
        return context
    
    def has_permission(self):
        self.team = self.get_object().team_members.first()
        if self.request.user == self.team.leader and self.team.editable:
            return True
        else:
            return self.request.user.has_perm('dashboard.change_team')
        
    def form_valid(self, form):
        team_member = form.save()
        if 'first_name' in form.changed_data or 'last_name' in form.changed_data:
            team_member.email = generate_team_member_email(team_member.first_name, team_member.last_name, self.team.name)
        
        team_member.gdpr.gdpr_consent = form.cleaned_data['gdpr_consent']
        team_member.gdpr.parental_consent = form.cleaned_data['parental_consent']
        team_member.gdpr.save()
        team_member.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        self.team = self.get_object().team_members.first()
        kwargs = {'pk': self.team.id}
        return reverse_lazy('dashboard:teams-detail', kwargs=kwargs)

@method_decorator(login_required, name='dispatch')
class TeamsMembersDeleteView(PermissionRequiredMixin, DeleteView):
    model = CustomUser
    context_object_name = 'team_member'
    template_name = 'dashboard/teams/members/delete.html'

    def get_context_data(self, **kwargs):
        context = super(TeamsMembersDeleteView, self).get_context_data(**kwargs)
        context['page_name'] = f"Usuwanie z zespołu: {context['team_member'].first_name} {context['team_member'].last_name}"
        context['team'] = self.get_object().team_members.first()
        return context
    
    def form_valid(self, form):
        self.team_member = self.get_object()
        self.team = self.team_member.team_members.first()
        self.team_member.gdpr.delete()
        self.team_member.delete()
        return HttpResponseRedirect(self.get_success_url(self.team))
    
    
    def has_permission(self):
        self.team = self.get_object().team_members.first()
        if self.request.user == self.team.leader and self.team.editable:
            return True
        else:
            return self.request.user.has_perm('dashboard.change_team')
    
    def get_success_url(self, team):
        kwargs = {'pk': team.id}
        return reverse_lazy('dashboard:teams-detail', kwargs=kwargs)
    

@method_decorator(login_required, name='dispatch')
class TeamsLeaderDisconnectView(PermissionRequiredMixin, DeleteView):
    model = Team
    context_object_name = 'team'
    template_name = 'dashboard/teams/members/delete-leader.html'

    def get_context_data(self, **kwargs):
        context = super(TeamsLeaderDisconnectView, self).get_context_data(**kwargs)
        context['page_name'] = f"Usuwanie kapitana z zespołu: {context['team'].leader.first_name} {context['team'].leader.last_name}"
        return context
    
    def form_valid(self, form):
        self.team = self.get_object()
        self.team.leader.gdpr.gdpr_consent = False
        self.team.leader.gdpr.parental_consent = False
        self.team.leader.gdpr.save()
        self.team.leader = None
        self.team.save()
        return HttpResponseRedirect(self.get_success_url())

    def has_permission(self):
        return self.request.user.has_perm('dashboard.change_team')
    
    def get_success_url(self):
        self.team = self.get_object()
        kwargs = {'pk': self.team.id}
        return reverse_lazy('dashboard:teams-detail', kwargs=kwargs)
    
@method_decorator(login_required, name='dispatch')
class TeamsLeaderUpdateView(PermissionRequiredMixin, UpdateView):
    model = CustomUser
    context_object_name = 'leader'
    template_name = 'dashboard/teams/members/edit-leader.html'
    form_class = UpdateTeamLeaderForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            requested_team = Team.objects.get(pk=self.kwargs["team_id"])
        except Team.DoesNotExist:
            return HttpResponseNotFound()
        
        if requested_team != self.get_object().team_set.first():
            return HttpResponseNotFound()
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeamsLeaderUpdateView, self).get_context_data(**kwargs)
        context['page_name'] = f"Edytuj kapitana zespołu: {context['leader'].first_name} {context['leader'].last_name}"
        context['team'] = self.get_object().team_set.first()
        return context
    
    def has_permission(self):
        return self.request.user.has_perm('dashboard.change_team')
        
    def form_valid(self, form):
        leader = form.save()
        leader.gdpr.gdpr_consent = form.cleaned_data['gdpr_consent']
        leader.gdpr.parental_consent = form.cleaned_data['parental_consent']
        leader.gdpr.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        self.team = self.get_object().team_set.first()
        kwargs = {'pk': self.team.id}
        return reverse_lazy('dashboard:teams-detail', kwargs=kwargs)
    
@method_decorator(login_required, name='dispatch')
class TeamsLeaderConnectView(PermissionRequiredMixin, UpdateView):
    model = Team
    context_object_name = 'team'
    template_name = 'dashboard/teams/members/add-leader.html'
    form_class = ConnectTeamLeaderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = f"Wybierz kapitana zespołu: {context['team'].name}"
        return context
    
    def has_permission(self):
        return self.request.user.has_perm('dashboard.change_team')
        
    def form_valid(self, form):
        team = form.save()
        if team.leader.gdpr is None:
            team_leader_gdpr = Gdpr.objects.create()
            team_leader_gdpr.save()
            team.leader.gdpr = team_leader_gdpr
            team.leader.save()

        team.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        self.team = self.get_object()
        kwargs = {'pk': self.team.id}
        return reverse_lazy('dashboard:teams-detail', kwargs=kwargs)