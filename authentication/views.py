from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.exceptions import NON_FIELD_ERRORS
from .forms import RegisterForm, LoginForm
from .utils import check_token, send_verification_mail, send_reset_password_mail
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

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                user_group = Group.objects.get(name=CustomGroup.names[user.user_type])
                user_group.user_set.add(user)
                form = RegisterForm()
                status = send_verification_mail(to_user=user)
                if status:
                    return render(request, 'auth/register.html', {'form': form, 'success': True})          
        else:
            form = RegisterForm()
        return render(request, 'auth/register.html', {'form': form})
    
def verify_email(request, user_id=None, token=None):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            try:
                user = get_user_model().objects.get(email=email)
            except get_user_model().models.CustomUser.DoesNotExist:
                user = None
            status = False
            if user is not None and not user.is_active:
                status = send_verification_mail(to_user=user)
            if status:
                url = reverse('auth:verify_email_resend_link') + '?verifylinksend=1'
            else:
                url = reverse('auth:verify_email_resend_link')
            return redirect(url)
        
        else:
            if 'verifylinksend' in request.GET:
                return render(request, 'auth/verify-email.html', {'verifylinksend': True})
            else:
                decoded_token = check_token(token=token)
                if decoded_token and decoded_token['user_id'] == user_id:
                    user = get_user_model().objects.get(pk=user_id)
                    if not user.is_active:
                        user.is_active = True
                        user.save()
                        return render(request, 'auth/verify-email.html', {'status': True})

                else:
                    return render(request, 'auth/verify-email.html', {'status': False})
                
def password_reset_request(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            try:
                user = get_user_model().objects.get(email=email)
            except get_user_model().models.CustomUser.DoesNotExist:
                user = None
            resetlinksend = False
            if user is not None:
                resetlinksend = send_reset_password_mail(to_user=user)

            return render(request, 'auth/password-reset-request.html', {'resetlinksend': resetlinksend})

        else:
            return render(request, 'auth/password-reset-request.html', {'resetlinksend': False})

def password_reset_change(request, user_id, token):
    if request.method == 'POST':
        user = get_user_model().objects.get(pk=user_id)
        form = SetPasswordForm(user=user, data=request.POST)
        
        if form.is_valid():
            form.save()
            return render(request, 'auth/password-reset.html', {'password_changed': True})
        
        return render(request, 'auth/password-reset.html', {'form': form})
            
    else:
        decoded_token = check_token(token=token)
        if decoded_token and decoded_token['user_id'] == user_id:
            user = get_user_model().objects.get(pk=user_id)
            form = SetPasswordForm(user)
            return render(request, 'auth/password-reset.html', {'form': form})
        else:
            return render(request, 'auth/password-reset.html', {'token_error': True})
    
    