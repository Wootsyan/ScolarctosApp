from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

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
        return render(request, 'auth/register.html')