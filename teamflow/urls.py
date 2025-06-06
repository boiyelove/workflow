from django.urls import path
from . import views

app_name = "teamflow"
urlpatterns = [
	path('create/', views.NewUnconfirmedUser.as_view(), name='get-invited'),
	path('create/team/', views.CreateTeam.as_view(), name='create-team'),
	path('create/<slug:slug>/', views.CreateAccount.as_view(), name='create-account'),
	path('teams/', views.TeamList.as_view(), name='team-profile'),	
	path('teams/<slug:team_slug>/', views.TeamDetail.as_view(), name='team-single'),	
	path('teams/<slug:team_slug>/members/', views.TeamMemberList.as_view(), name='team-members'),
	path('teams/<slug:team_slug>/members/<slug:member_slug>/', views.TeamMemberDetail.as_view(), name='team-member'),
	
	path('teams/<slug:team_slug>/flows/', views.TeamMemberDetail.as_view(), name='team-flows'),
	path('teams/<slug:team_slug>/flows/<slug:slug>/', views.TeamMemberDetail.as_view(), name='team-flow'),
	
	path('invited/<slug:slug>/', views.JoinTeam.as_view, name='join-team'),
	path('login/', views.LoginView.as_view(), name="login"),
	path('logout/', views.LogoutView.as_view(), name="logout"),
	]
