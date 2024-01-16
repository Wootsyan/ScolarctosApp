from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('users/admins/', views.UserAdminsListView.as_view(), name='users-list-admins'),
    path('users/organizers/', views.UserOrganizersListView.as_view(), name='users-list-organizers'),
    path('users/students/', views.UserStudentsListView.as_view(), name='users-list-students'),
    path('users/guardians/', views.UserGuardiansListView.as_view(), name='users-list-guardians'),
]