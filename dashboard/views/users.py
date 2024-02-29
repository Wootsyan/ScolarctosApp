from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from users.models import CustomUser, CustomGroup
from users.forms import SpecialUserCreateForm
from authentication.utils import send_verification_mail

'''
### Users Views
'''
@method_decorator(login_required, name='dispatch')
class UserAdminsListView(PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users_list'
    template_name = 'dashboard/users/list.html'
    permission_required = ('users.view_admins')

    def get_context_data(self, **kwargs):
        context = super(UserAdminsListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Administratorzy'
        return context
    
    def get_queryset(self):
        return CustomUser.objects.filter(user_type=CustomUser.ADMIN).exclude(id=self.request.user.id)
    
@method_decorator(login_required, name='dispatch')
class CreateUserAdminView(PermissionRequiredMixin, FormView):
    template_name = 'dashboard/users/add.html'
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
        context['page_name'] = 'Nowy administrator'
        return context


@method_decorator(login_required, name='dispatch')
class UserOrganizersListView(PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users_list'
    template_name = 'dashboard/users/list.html'
    permission_required = ('users.view_organizers')

    def get_context_data(self, **kwargs):
        context = super(UserOrganizersListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Organizatorzy'
        return context
    
    def get_queryset(self):
        return CustomUser.objects.filter(user_type=CustomUser.ORGANIZER).exclude(id=self.request.user.id)

@method_decorator(login_required, name='dispatch')
class CreateUserOrganizerView(PermissionRequiredMixin, FormView):
    template_name = 'dashboard/users/add.html'
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
        context['page_name'] = 'Nowy organizator'
        return context

@method_decorator(login_required, name='dispatch')
class UserStudentsListView(PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users_list'
    template_name = 'dashboard/users/list.html'
    permission_required = ('users.view_customuser')

    def get_context_data(self, **kwargs):
        context = super(UserStudentsListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Uczniowie'
        return context
    
    def get_queryset(self):
        return CustomUser.objects.filter(user_type=CustomUser.STUDENT).exclude(id=self.request.user.id)

@method_decorator(login_required, name='dispatch')
class UserGuardiansListView(PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users_list'
    template_name = 'dashboard/users/list.html'
    permission_required = ('users.view_customuser')

    def get_context_data(self, **kwargs):
        context = super(UserGuardiansListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Opiekunowie'
        return context
    
    def get_queryset(self):
        return CustomUser.objects.filter(user_type=CustomUser.GUARDIAN).exclude(id=self.request.user.id)
    
@method_decorator(login_required, name='dispatch')
class UserDetailView(PermissionRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'dashboard/users/detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['page_name'] = f"Użytkownik: {context['user'].first_name} {context['user'].last_name}"
        context['user'].user_type_name = context['user'].USER_TYPE_CHOICES[context['user'].user_type - 1][1]
        return context
    
    def has_permission(self):
        context_user_object = self.get_object()
        if context_user_object.user_type == CustomUser.ADMIN:
            return self.request.user.has_perm('users.view_admins')
        elif context_user_object.user_type == CustomUser.ORGANIZER:
            return self.request.user.has_perm('users.view_organizers')
        elif context_user_object.user_type == CustomUser.STUDENT_TEAM_MEMBER:
            return False
        else:
            return self.request.user.has_perm('users.view_customuser')

@method_decorator(login_required, name='dispatch')
class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'dashboard/users/edit.html'

    fields = [ 
        'first_name', 
        'last_name',
        'phone_number',
        'description',
    ]

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['page_name'] = f"Edycja: {context['user'].first_name} {context['user'].last_name}"
        for field in self.fields:
            context['form'].fields[field].widget.attrs['class'] = 'form-control'
        return context
    
    def has_permission(self):
        context_user_object = self.get_object()
        if context_user_object.user_type == CustomUser.ADMIN:
            return self.request.user.has_perm('users.change_admins')
        elif context_user_object.user_type == CustomUser.ORGANIZER:
            return self.request.user.has_perm('users.change_organizers')
        elif context_user_object.user_type == CustomUser.STUDENT_TEAM_MEMBER:
            return False
        else:
            return self.request.user.has_perm('users.change_customuser')
    
    def get_success_url(self) -> str:
        context_user_object = self.get_object()
        kwargs = {'pk': context_user_object.id}
        if '_save' in self.request.POST:
            return reverse_lazy('dashboard:users-detail', kwargs=kwargs)
        elif '_continue' in self.request.POST:
            return reverse_lazy('dashboard:users-edit', kwargs=kwargs)

@method_decorator(login_required, name='dispatch')
class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'dashboard/users/delete.html'

    def get_context_data(self, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['page_name'] = f"Użytkownik: {context['user'].first_name} {context['user'].last_name}"
        return context
    
    def has_permission(self):
        context_user_object = self.get_object()
        if context_user_object.user_type == CustomUser.ADMIN:
            return self.request.user.has_perm('users.delete_admins')
        elif context_user_object.user_type == CustomUser.ORGANIZER:
            return self.request.user.has_perm('users.delete_organizers')
        elif context_user_object.user_type == CustomUser.STUDENT_TEAM_MEMBER:
            return False
        else:
            return self.request.user.has_perm('users.delete_customuser')
    
    def get_success_url(self) -> str:
        context_user_object = self.get_object()
        if context_user_object.user_type == CustomUser.ADMIN:
            return reverse_lazy('dashboard:users-list-admins')
        elif context_user_object.user_type == CustomUser.ORGANIZER:
            return reverse_lazy('dashboard:users-list-organizers')
        elif context_user_object.user_type == CustomUser.STUDENT:
            return reverse_lazy('dashboard:users-list-students')
        elif context_user_object.user_type == CustomUser.GUARDIAN:
            return reverse_lazy('dashboard:users-list-guardians')
    