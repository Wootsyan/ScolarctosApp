from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from users.models import CustomUser
from authentication.forms import ConfirmationForm
from authentication.utils import  send_confirmation_code_mail, generate_confirmation_code

'''
### Profile Views
'''
@method_decorator(login_required, name='dispatch')
class ProfileDetailView(PermissionRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'dashboard/profile/detail.html'

    def get_object(self):
        return self.model.objects.get(pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['page_name'] = f"Profil: {context['user'].first_name} {context['user'].last_name}"
        context['user'].user_type_name = context['user'].USER_TYPE_CHOICES[context['user'].user_type - 1][1]
        return context
    
    def has_permission(self):
        context_user_object = self.get_object()
        if context_user_object.id == self.request.user.id:
            return True
        
@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(PermissionRequiredMixin, UpdateView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'dashboard/profile/edit.html'

    fields = [ 
        'first_name', 
        'last_name',
        'phone_number',
        'description',
    ]

    def get_object(self):
        return self.model.objects.get(pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['page_name'] = "Edytuj swój profil"
        for field in self.fields:
            context['form'].fields[field].widget.attrs['class'] = 'form-control'
        return context
    
    def has_permission(self):
        context_user_object = self.get_object()
        if context_user_object.id == self.request.user.id:
            return True
    
    def get_success_url(self) -> str:
        if '_save' in self.request.POST:
            return reverse_lazy('dashboard:profile-detail')
        elif '_continue' in self.request.POST:
            return reverse_lazy('dashboard:profile-edit')

@method_decorator(login_required, name='dispatch')
class ProfileDeleteView(PermissionRequiredMixin, DeleteView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'dashboard/profile/delete.html'
    form_class = ConfirmationForm
    confirmation_code = generate_confirmation_code()

    def get_object(self):
        return self.model.objects.get(pk=self.request.user.id)
    
    def dispatch(self, request, *args, **kwargs):
        messages_storage = messages.get_messages(self.request)
        if request.method == 'GET' and not messages_storage:
            send_confirmation_code_mail(to_user=self.request.user, confirmation_code=self.confirmation_code)
        return super(ProfileDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileDeleteView, self).get_context_data(**kwargs)
        context['page_name'] = "Usuwanie konta"
        return context
    
    def has_permission(self):
        context_user_object = self.get_object()
        if context_user_object.id == self.request.user.id:
            return True
    
    def get_success_url(self) -> str:
        return reverse_lazy('logout')
    
    def form_valid(self, form):
        form_confirm_code = form.cleaned_data['confirm_code']
        if self.confirmation_code == form_confirm_code:
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        else:
            messages.add_message(self.request, messages.ERROR, f'Kod potwierdzający: {form_confirm_code} jest nieprawidłowy')
            return HttpResponseRedirect(reverse_lazy('dashboard:profile-delete'))
