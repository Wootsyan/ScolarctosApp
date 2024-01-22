from django.urls import path

from .views import main, users, profile 

app_name = 'dashboard'

urlpatterns = [
    path('', main.IndexView.as_view(), name='index'),
    path('users/admins/', users.UserAdminsListView.as_view(), name='users-list-admins'),
    path('users/admins/new/', users.CreateUserAdminView.as_view(), name='users-admins-new'),
    path('users/organizers/', users.UserOrganizersListView.as_view(), name='users-list-organizers'),
    path('users/organizers/new/', users.CreateUserOrganizerView.as_view(), name='users-organizers-new'),
    path('users/students/', users.UserStudentsListView.as_view(), name='users-list-students'),
    path('users/guardians/', users.UserGuardiansListView.as_view(), name='users-list-guardians'),
    path('users/<int:pk>/', users.UserDetailView.as_view(), name='users-detail'),
    path('users/<int:pk>/edit/', users.UserUpdateView.as_view(), name='users-edit'),
    path('users/<int:pk>/delete/', users.UserDeleteView.as_view(), name='users-delete'),
    path('profile/', profile.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/edit/', profile.ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/delete/', profile.ProfileDeleteView.as_view(), name='profile-delete'),
]