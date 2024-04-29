import json
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView
from django.views import View


from users.models import CustomUser
from dashboard.models import Team, Invitation, TeamGuardian

'''
### Invitations Views
'''

@method_decorator(login_required, name='dispatch')
class InvitationsAvailableGuardiansListView(PermissionRequiredMixin, ListView):
    context_object_name = 'guardians'
    template_name = 'dashboard/invitations/available-guardians-list.html'

    def dispatch(self, request, *args, **kwargs):
        self.leader = self.request.user
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Find all guardians connected to same school as user's team school
        # Guardian can connect with many teams
        leader_school = self.leader.team_set.first().school
        leader_received_invitations = self.leader.recipient.filter(accepted__isnull=True)
        return leader_school.guardians.exclude(sender__in=leader_received_invitations)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Opiekunowie z Twojej szkoły'
        for guardian in context['guardians']:
            if guardian.recipient.filter(sender=self.leader).filter(accepted=None).exists():
                guardian.invited = True
        return context
    
    def has_permission(self):
        if self.leader.user_type == CustomUser.STUDENT and self.leader.team_set.exists() and self.leader.team_set.first().team_guardian is None:
            return True
        return False
    
@method_decorator(login_required, name='dispatch')
class InvitationsAvailableTeamsListView(PermissionRequiredMixin, ListView):
    context_object_name = 'teams'
    template_name = 'dashboard/invitations/available-teams-list.html'

    def dispatch(self, request, *args, **kwargs):
        self.guardian = self.request.user
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Find all teams connected to same school as guardian's schools
        # Team can connect only one guardian
        guardian_schools = self.guardian.schools.all()
        guardian_received_invitations = self.guardian.recipient.all()
        teams = Team.objects.filter(
            school__in=guardian_schools, 
            team_guardian__isnull=True, 
            leader__isnull=False
            ).exclude(leader__sender__in=guardian_received_invitations)
        return teams

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Zespoły z Twoich szkół'
        for team in context['teams']:
            if team.leader.recipient.filter(sender=self.guardian).filter(accepted=None).exists():
                team.invited = True
        return context
    
    def has_permission(self):
        if self.request.user.user_type == CustomUser.GUARDIAN:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class InvitationCreateView(PermissionRequiredMixin, CreateView):
    http_method_names = ['post']
    model = Invitation

    fields = [
        'sender',
        'recipient',
    ]
    def post(self, request, *args, **kwargs):
        post_data = json.loads(request.body)
        recipient_id = post_data.get('id')
        if recipient_id and CustomUser.objects.filter(pk=recipient_id).exists():
            data = {
                "sender": request.user.id,
                "recipient": recipient_id,
            }
            FormClass = self.get_form_class()
            form = FormClass(data)
            if form.is_valid():
                if (not Invitation.accepted_none_objects.filter(sender=form.cleaned_data.get('sender')).filter(recipient=form.cleaned_data.get('recipient')).exists() and
                    not Invitation.accepted_none_objects.filter(sender=form.cleaned_data.get('recipient')).filter(recipient=form.cleaned_data.get('sender')).exists()):
                    form.save()
                    return JsonResponse({
                        'messageInvite': 'Zaproszony', 
                        'messageCancel': 'Anuluj',
                        'dataRecipientID': recipient_id,
                    })
        
        return HttpResponseBadRequest('Invalid request')
    
    def has_permission(self):
        user = self.request.user
        if user.user_type == CustomUser.GUARDIAN and user.schools.exists():
            return True
        if user.user_type == CustomUser.STUDENT and user.team_set.exists() and user.team_set.first().team_guardian is None:
            return True
        return False
    
@method_decorator(login_required, name='dispatch')
class InvitationCancelView(PermissionRequiredMixin, View):
    http_method_names = ['delete']
    model = Invitation

    def delete(self, request, *args, **kwargs):
        delete_data = json.loads(request.body)
        recipient_id = delete_data.get('id')
        if recipient_id and CustomUser.objects.filter(pk=recipient_id).exists():
            try:
                obj = self.model.accepted_none_objects.get(sender=request.user.id, recipient=recipient_id)
                obj.delete()
                return JsonResponse({'message': 'Zaproś', 'dataRecipientID': recipient_id})
            except self.model.DoesNotExist:
                return HttpResponseBadRequest('Invalid request')
    
    def has_permission(self):
        user = self.request.user
        if user.sender.filter(accepted=None).exists():
            return True
        return False
    
class InvitationListView(PermissionRequiredMixin, ListView):
    context_object_name = 'invitations'
    template_name = 'dashboard/invitations/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Aktywne zaproszenia'
        return context

    def get_queryset(self):
        return self.request.user.recipient.filter(accepted=None)
    
    def has_permission(self):
        return self.request.user.has_perm('dashboard.view_invitation')
    
class InvitationEditView(PermissionRequiredMixin, UpdateView):
    model = Invitation
    context_object_name = 'invitation'
    template_name = 'dashboard/invitations/edit.html'
    fields = [
        'accepted'
    ]

    def form_valid(self, form):
        if "accept" in self.kwargs:
            if self.kwargs["accept"]:
                self.object.accepted = True
                team_guardian = TeamGuardian()
                team_guardian.guardian = self.object.get_guardian()
                team_guardian.save()
                team = self.object.get_team()
                team.team_guardian = team_guardian
                team.save()
            else:
                self.object.accepted = False
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "accept" in self.kwargs:
            accept = self.kwargs["accept"]
            context['accept'] = accept
            if accept:
                context['page_name'] = 'Zaakceptuj zaproszenie'
            else:
                context['page_name'] = 'Odrzuć zaproszenie'
        return context

    def has_permission(self):
        self.object = self.get_object()
        return self.object.recipient == self.request.user
    
    def get_success_url(self):
        if '_accept' in self.request.POST:
            if self.request.user.is_student():
                return reverse_lazy('dashboard:teams-detail', kwargs={'pk': self.request.user.team_set.first().id})
            
            if self.request.user.is_guardian():
                #TODO change url to "my teams"
                return reverse_lazy('dashboard:index')
            
        if '_not-accept' in self.request.POST:
            return reverse_lazy('dashboard:invitations-list')