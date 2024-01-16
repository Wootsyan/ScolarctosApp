from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from users.models import CustomUser, CustomGroup
from users.forms import SpecialUserCreateForm
from authentication.utils import send_verification_mail

@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
        template_name = "dashboard/index.html"

@method_decorator(login_required, name='dispatch')
class UserAdminsListView(PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users_list'
    queryset = CustomUser.objects.filter(user_type=CustomUser.ADMIN)
    template_name = 'dashboard/users/list.html'
    permission_required = ('users.view_admins')

    def get_context_data(self, **kwargs):
        context = super(UserAdminsListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Administratorzy'
        context['page_type'] = 'admins'
        return context
    
@method_decorator(login_required, name='dispatch')
class CreateUserAdminView(PermissionRequiredMixin, FormView):
    template_name = 'dashboard/users/edit.html'
    permission_required = ('users.add_admins')
    success_url = reverse_lazy('dashboard:users-list-admins')
    form_class = SpecialUserCreateForm

    def form_valid(self, form):
        user = form.save()
        user.user_type = CustomUser.ADMIN
        user.save()
        user_group = Group.objects.get(name=CustomGroup.names[CustomUser.ADMIN])
        user_group.user_set.add(user)
        send_verification_mail(to_user=user)
        return super(CreateUserAdminView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CreateUserAdminView, self).get_context_data(**kwargs)
        context['page_name'] = 'Utwórz nowego administratora'
        context['page_type'] = 'admins'
        return context


@method_decorator(login_required, name='dispatch')
class UserOrganizersListView(PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users_list'
    queryset = CustomUser.objects.filter(user_type=CustomUser.ORGANIZER)
    template_name = 'dashboard/users/list.html'
    permission_required = ('users.view_organizers')

    def get_context_data(self, **kwargs):
        context = super(UserOrganizersListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Organizatorzy'
        context['page_type'] = 'organizers'
        return context

@method_decorator(login_required, name='dispatch')
class CreateUserOrganizerView(PermissionRequiredMixin, FormView):
    template_name = 'dashboard/users/edit.html'
    permission_required = ('users.add_organizers')
    success_url = reverse_lazy('dashboard:users-list-organizers')
    form_class = SpecialUserCreateForm

    def form_valid(self, form):
        user = form.save()
        user.user_type = CustomUser.ORGANIZER
        user.save()
        user_group = Group.objects.get(name=CustomGroup.names[CustomUser.ORGANIZER])
        user_group.user_set.add(user)
        send_verification_mail(to_user=user)
        return super(CreateUserOrganizerView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CreateUserOrganizerView, self).get_context_data(**kwargs)
        context['page_name'] = 'Utwórz nowego organizatora'
        context['page_type'] = 'organizers'
        return context

@method_decorator(login_required, name='dispatch')
class UserStudentsListView(PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users_list'
    queryset = CustomUser.objects.filter(user_type=CustomUser.STUDENT)
    template_name = 'dashboard/users/list.html'
    permission_required = ('users.view_customuser')

    def get_context_data(self, **kwargs):
        context = super(UserStudentsListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Uczniowie'
        return context


@method_decorator(login_required, name='dispatch')
class UserGuardiansListView(PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users_list'
    queryset = CustomUser.objects.filter(user_type=CustomUser.GUARDIAN)
    template_name = 'dashboard/users/list.html'
    permission_required = ('users.view_customuser')

    def get_context_data(self, **kwargs):
        context = super(UserGuardiansListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Opiekunowie'
        return context
    
def error_403(request, exception):
    return render(request, 'dashboard/errors/403.html')