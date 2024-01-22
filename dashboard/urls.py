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
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='users-detail'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='users-edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='users-delete'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),
]