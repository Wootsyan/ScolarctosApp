from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from .forms import RegisterForm
from .utils import generate_token, check_token

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
                email_verify_token = generate_token(user.id, user.email)
                email_data = {
                    'user_name': user.first_name,
                    'verification_time': settings.VERIFICATION_EXPIRE_MINUTES,
                    'verification_url': settings.SITE_URL + reverse('verify_email', args=(user.id, email_verify_token))
                } 

                html_message = render_to_string("auth/email/email-confirmation.html", email_data, request=request)
                plain_message = strip_tags(html_message)
                mail = EmailMultiAlternatives(
                    subject="Potwierdź swoje konto - Zespół Koala",
                    body=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )
                mail.attach_alternative(html_message, "text/html")
                mail.send()
                form = RegisterForm()
                return render(request, 'auth/register.html', {'form': form, 'success': True})
        else:
            form = RegisterForm()
        return render(request, 'auth/register.html', {'form': form})
    
def verify_email(request, user_id, token):
    pass

# def emailtest(request):
#     return render(request, 'auth/email/email-confirmation.html')