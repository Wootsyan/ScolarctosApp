from django.urls import path

from .views import main, users, profile, schools, teams, invitations

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
    path('schools/', schools.SchoolsListView.as_view(), name='schools-list'),
    path('schools/type/<int:type>/', schools.SchoolsListView.as_view(), name='schools-list-type'),
    path('schools/my-schools/', schools.SchoolsGuardianListView.as_view(), name='schools-guardian-list'),
    path('schools/my-schools/edit/', schools.SchoolsGuardianUpdateView.as_view(), name='schools-guardian-edit'),
    path('schools/new/', schools.SchoolsCreateView.as_view(), name='schools-new'),
    path('schools/<int:pk>/', schools.SchoolsDetailView.as_view(), name='schools-detail'),
    path('schools/<int:pk>/edit/', schools.SchoolsUpdateView.as_view(), name='schools-edit'),
    path('schools/<int:pk>/delete/', schools.SchoolsDeleteView.as_view(), name='schools-delete'),
    path('teams/', teams.TeamsListView.as_view(), name='teams-list'),
    path('teams/new/', teams.TeamsCreateView.as_view(), name='teams-new'),
    path('teams/<int:pk>/', teams.TeamsDetailView.as_view(), name='teams-detail'),
    path('teams/<int:pk>/edit/', teams.TeamsUpdateView.as_view(), name='teams-edit'),
    path('teams/<int:pk>/delete/', teams.TeamsDeleteView.as_view(), name='teams-delete'),
    path('teams/<int:pk>/leader/add/', teams.TeamsLeaderConnectView.as_view(), name='teams-leader-new'),
    path('teams/<int:team_id>/leader/<int:pk>/edit/', teams.TeamsLeaderUpdateView.as_view(), name='teams-leader-edit'),
    path('teams/<int:pk>/leader/delete/', teams.TeamsLeaderDisconnectView.as_view(), name='teams-leader-delete'),
    path('teams/<int:pk>/members/new/', teams.TeamsMembersCreateView.as_view(), name='teams-members-new'),
    path('teams/members/<int:pk>/edit/', teams.TeamsMembersUpdateView.as_view(), name='teams-members-edit'),
    path('teams/members/<int:pk>/delete/', teams.TeamsMembersDeleteView.as_view(), name='teams-members-delete'),
    path('teams/<int:team_id>/file/<int:pk>/delete/', teams.TeamsFileDeleteView.as_view(), name='teams-file-delete'),
    path('invitations/available-guardians/', invitations.InvitationsAvailableGuardiansListView.as_view(), name='invitations-available-guardians-list'),
    path('invitations/available-teams/', invitations.InvitationsAvailableTeamsListView.as_view(), name='invitations-available-teams-list'),
    path('invitations/invite/', invitations.InvitationCreateView.as_view(), name='invitations-invite'),
]