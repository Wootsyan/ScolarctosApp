from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.exceptions import NON_FIELD_ERRORS, PermissionDenied
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from .forms import RegisterForm, LoginForm, EmailForm
from .utils import check_token, send_verification_mail, send_reset_password_mail
from .decorators import redirect_logged_user
from users.models import CustomGroup

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["non_field_error_inactive"] = context["form"].has_error(NON_FIELD_ERRORS, code='inactive')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('dashboard:index')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('auth:login')

@method_decorator(redirect_logged_user, name='dispatch')
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'auth/register.html'	
    
    def form_valid(self, form):
        user = form.save()
        user_group = Group.objects.get(name=CustomGroup.names[user.user_type])
        user_group.user_set.add(user)
        verification_mail_sent = send_verification_mail(to_user=user)
        if verification_mail_sent:
            messages.add_message(self.request, messages.SUCCESS, 'Mail z linkiem aktywacyjnym został wysłany')
        else:
            messages.add_message(self.request, messages.ERROR, 'Mail z linkiem aktywacyjnym nie został wysłany')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        
    def get_success_url(self):
        return reverse_lazy('auth:register')
    
@method_decorator(redirect_logged_user, name='dispatch')
class VerifyEmailView(FormView):
    form_class = EmailForm
    template_name = 'auth/verify-email.html'
    
    def get(self, request, *args, **kwargs):
        if 'user_id' in kwargs and 'token' in kwargs:
            user_id = kwargs.get('user_id') 
            token = kwargs.get('token')
            decoded_token = check_token(token=token)
            if decoded_token and decoded_token['user_id'] == user_id:
                user = get_user_model().objects.get(pk=user_id)
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Użytkownik został aktywowany', extra_tags='user-activated')
                else:
                    messages.add_message(request, messages.ERROR, 'Użytkownik jest już aktywny', extra_tags='user-already-active')
            else:
                messages.add_message(request, messages.ERROR, 'Token wygasł lub jest nieprawidłowy', extra_tags='token-invalid')

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages_list = messages.get_messages(self.request)
        if len(messages_list):
            for message in messages_list:
                if message.tags == 'verify-link-sent success':
                    context['verify_link_sent'] = True
                if message.tags == 'user-activated success':
                    context['user_activated'] = True
                if message.tags == 'user-already-active error':
                    context['user_already_active'] = True
                if message.tags == 'token-invalid error':
                    context['token_invalid'] = True
                    context['verify_email_request'] = True
        else:
            context['verify_email_request'] = True
            
        return context

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().models.CustomUser.DoesNotExist:
            user = None
        if user is not None and not user.is_active:
            verification_mail_sent = send_verification_mail(to_user=user)
        if verification_mail_sent:
            messages.add_message(self.request, messages.SUCCESS, 'Mail z linkiem aktywacyjnym został wysłany', extra_tags='verify-link-sent')
        else:
            messages.add_message(self.request, messages.ERROR, 'Mail z linkiem aktywacyjnym nie został wysłany', extra_tags='verify-link-not-sent')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('auth:verify-email-request')

@method_decorator(redirect_logged_user, name='dispatch')
class PasswordResetRequestView(FormView):
    form_class = EmailForm
    template_name = 'auth/password-reset-request.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages_list = messages.get_messages(self.request)
        if len(messages_list):
            for message in messages_list:
                if message.tags == 'reset-password-link-sent success':
                    context['reset_password_link_sent'] = True
            
        return context

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().models.CustomUser.DoesNotExist:
            user = None
        if user is not None:
            reset_link_sent = send_reset_password_mail(to_user=user)
        if reset_link_sent:
            messages.add_message(self.request, messages.SUCCESS, 'Mail z linkiem do resetu hasła został wysłany', extra_tags='reset-password-link-sent')
        else:
            messages.add_message(self.request, messages.ERROR, 'Mail z linkiem do resetu hasła nie został wysłany', extra_tags='reset-password-link-not-sent')
        return super().form_valid(form)
  
    def get_success_url(self):
        return reverse_lazy('auth:password-reset-request')
    
@method_decorator(redirect_logged_user, name='dispatch')
class PasswordResetChangeView(FormView, SingleObjectMixin):
    form_class = SetPasswordForm
    template_name = 'auth/password-reset.html'
    model = get_user_model()

    def get_object(self, queryset=None):
        if not hasattr(self, 'object'):
            self.object = get_object_or_404(get_user_model(), pk=self.kwargs['pk'])
        return self.object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'token' in kwargs:
            self.token = kwargs.get('token')
            decoded_token = check_token(token=self.token)
            if not(decoded_token and decoded_token['user_id'] == self.object.id):
                messages.add_message(request, messages.ERROR, 'Token wygasł lub jest nieprawidłowy', extra_tags='token-invalid')
        
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Hasło zostało zmienione', extra_tags='password-changed')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        kwargs['user'] = self.get_object()
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages_list = messages.get_messages(self.request)
        if len(messages_list):
            for message in messages_list:
                if message.tags == 'token-invalid error':
                    context['token_invalid'] = True
        else:
            context['password_reset_change_form'] = True
            
        return context
    
    def get_success_url(self):
        return reverse_lazy('auth:password-reset-changed')
    
@method_decorator(redirect_logged_user, name='dispatch')
class PasswordChangedView(TemplateView):
    template_name = 'auth/password-reset.html'

    def dispatch(self, request, *args, **kwargs):      
        if not len(messages.get_messages(request)):
            raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages_list = messages.get_messages(self.request)
        if len(messages_list):
            for message in messages_list:
                if message.tags == 'password-changed success':
                    context['password_changed'] = True
            
        return context
