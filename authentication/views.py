from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from .forms import RegisterForm

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
                # auth_login(request, user)
                # return redirect('register_success')
                form = RegisterForm()
                return render(request, 'auth/register.html', {'form': form, 'success': True})
        else:
            form = RegisterForm()
        return render(request, 'auth/register.html', {'form': form})
    