from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from . import views

app_name = 'auth'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('dashboard:index'))),
    path('login/', views.CustomLoginView.as_view() , name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email-request'),
    path('verify-email/<int:user_id>/<str:token>/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('password-reset/request/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/change-password/<int:user_id>/<str:token>/', views.password_reset_change, name="password_reset_change"),
]