from django.shortcuts import redirect
from django.urls import reverse_lazy

def redirect_logged_user(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
                return redirect(reverse_lazy('dashboard:index'))
        return view(request, *args, **kwargs)
    return wrapper