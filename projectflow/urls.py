from django.urls import path
from . import views

app_name = 'projectflow'
urlpatterns = [
    path('', views.project_list, name='project-list'),
    path('create/', views.project_create, name='project-create'),
    path('project/<slug:slug>/', views.project_detail, name='project-detail'),
    path('project/<slug:slug>/update/', views.project_update, name='project-update'),
    path('project/<slug:slug>/delete/', views.project_delete, name='project-delete'),
]
