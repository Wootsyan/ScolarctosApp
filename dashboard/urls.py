from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/admins/', views.UserAdminsListView.as_view(), name='users-list-admins'),
    path('users/admins/new/', views.CreateUserAdminView.as_view(), name='users-admins-new'),
    path('users/organizers/', views.UserOrganizersListView.as_view(), name='users-list-organizers'),
    path('users/organizers/new/', views.CreateUserOrganizerView.as_view(), name='users-organizers-new'),
    path('users/students/', views.UserStudentsListView.as_view(), name='users-list-students'),
    path('users/guardians/', views.UserGuardiansListView.as_view(), name='users-list-guardians'),
]