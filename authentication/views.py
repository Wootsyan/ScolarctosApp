from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import RegisterForm
from .utils import check_token, send_verification_mail

def redirect_auth_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

def login(request):
    return render(request, 'auth/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                form = RegisterForm()
                status = send_verification_mail(to_user=user)
                if status:
                    return render(request, 'auth/register.html', {'form': form, 'success': True})          
        else:
            form = RegisterForm()
        return render(request, 'auth/register.html', {'form': form})
    
def verify_email(request, user_id=None, token=None):
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
            