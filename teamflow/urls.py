from django.urls import path
from . import views

app_name = 'teamflow'
urlpatterns = [
    path('', views.team_list, name='team-list'),
    path('create/', views.team_create, name='team-create'),
    path('<slug:url>/', views.team_detail, name='team-detail'),
    path('<slug:url>/update/', views.team_update, name='team-update'),
    path('<slug:url>/delete/', views.team_delete, name='team-delete'),
]
