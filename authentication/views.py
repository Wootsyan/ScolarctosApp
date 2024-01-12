from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group
from .forms import RegisterForm, LoginForm
from .utils import check_token, send_verification_mail, send_reset_password_mail
from users.models import CustomGroup

def redirect_auth_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    else:
        return redirect('login')

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        return redirect('dashboard:index')
                    else:
                        error_login_message = 'Konto nie jest aktywne'
                        inactive_user = True
                else:
                    error_login_message = 'Nieprawidłowy login lub hasło'
                    inactive_user = False
                return render(request, 'auth/login.html', {'form': form, 'error_login_message': error_login_message, 'inactive_user': inactive_user})

        else:
            form = LoginForm()

        return render(request, 'auth/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                user_group = Group.objects.get(name=CustomGroup.names[user.user_type-1])
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
                url = reverse('verify_email_resend_link') + '?verifylinksend=1'
            else:
                url = reverse('verify_email_resend_link')
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
    
    