from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin
from users.models import CustomUser, CustomGroup

@login_required
def index(request):
    return render(request, 'dashboard/index.html')

@method_decorator(login_required, name='dispatch')
class UserAdminsListView(PermissionRequiredMixin, generic.ListView):
    model = CustomUser
    context_object_name = 'users_list'
    queryset = CustomUser.objects.filter(user_type=CustomUser.ADMIN)
    template_name = 'dashboard/users/list.html'
    permission_required = ('users.view_admins')

    def get_context_data(self, **kwargs):
        context = super(UserAdminsListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Administratorzy'
        return context

@method_decorator(login_required, name='dispatch')
class UserOrganizersListView(PermissionRequiredMixin, generic.ListView):
    model = CustomUser
    context_object_name = 'users_list'
    queryset = CustomUser.objects.filter(user_type=CustomUser.ORGANIZER)
    template_name = 'dashboard/users/list.html'
    permission_required = ('users.view_organizers')

    def get_context_data(self, **kwargs):
        context = super(UserOrganizersListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Organizatorzy'
        return context

@method_decorator(login_required, name='dispatch')
class UserStudentsListView(PermissionRequiredMixin, generic.ListView):
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
class UserGuardiansListView(PermissionRequiredMixin, generic.ListView):
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