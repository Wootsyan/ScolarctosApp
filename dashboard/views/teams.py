from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from dashboard.models import Team
from dashboard.forms import CreateTeamForm
from users.models import CustomUser

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
        if self.request.user.user_type == CustomUser.STUDENT:
            self.object.leader = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        self.object = self.get_object()
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