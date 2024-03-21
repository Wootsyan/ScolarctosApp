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
    path('password-reset/request/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/change-password/<int:pk>/<str:token>/', views.PasswordResetChangeView.as_view(), name="password-reset-change"),
    path('password-reset/password-changed/', views.PasswordChangedView.as_view(), name="password-reset-changed"),
]