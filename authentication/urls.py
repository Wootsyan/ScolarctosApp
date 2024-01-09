from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirect_auth_user),
    path('login/', views.login , name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('verify-email/<int:user_id>/<str:token>/', views.verify_email, name='verify_email'),
    path('verify-email/', views.verify_email, name='verify_email_resend_link'),
]