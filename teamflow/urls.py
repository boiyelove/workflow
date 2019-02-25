from django.conf.urls import url
from . import views

app_name = "teamflow"
urlpatterns = [
	url(r'^create/$', views.NewUnconfirmedUser.as_view(), name='get-invited'),
	url(r'^create/team/$', views.CreateTeam.as_view(), name='create-team'),
	url(r'^create/(?P<slug>[\w]+)/$', views.CreateAccount.as_view(), name='create-account'),
	url(r'^teams/$', views.TeamList.as_view(), name='team-profile'),	
	url(r'^teams/(?P<team_slug>[\w]+)/$', views.TeamDetail.as_view(), name='team-single'),	
	url(r'^teams/(?P<team_slug>[\w]+)/members/$', views.TeamMemberList.as_view(), name='team-members'),
	url(r'^teams/(?P<team_slug>[\w]+)/members/(?P<member_slug>[\w]+)/$', views.TeamMemberDetail.as_view(), name='team-member'),
	
	url(r'^teams/(?P<team_slug>[\w]+)/flows/$', views.TeamMemberDetail.as_view(), name='team-flows'),
	url(r'^teams/(?P<team_slug>[\w]+)/flows/(?P<slug>[\w]+)/$', views.TeamMemberDetail.as_view(), name='team-flow'),
	
	url(r'^invited/(?P<slug>[\w]+)/$', views.JoinTeam.as_view),
	url(r'^login/$', views.LoginView.as_view(), name="login"),
	url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
	]
