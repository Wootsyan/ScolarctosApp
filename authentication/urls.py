from django.urls import path

from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.redirect_auth_user),
    path('login/', views.CustomLoginView.as_view() , name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('verify-email/<int:user_id>/<str:token>/', views.verify_email, name='verify_email'),
    path('verify-email/', views.verify_email, name='verify_email_resend_link'),
    path('password-reset/request/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/change-password/<int:user_id>/<str:token>/', views.password_reset_change, name="password_reset_change"),
]