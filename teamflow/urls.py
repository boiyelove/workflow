from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeamListView.as_view(), name='team_list'),
    path('create/', views.TeamCreateView.as_view(), name='team_create'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('<int:pk>/invite/', views.TeamInviteView.as_view(), name='team_invite'),
]
