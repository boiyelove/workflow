from django.urls import path
from . import views

app_name = 'workspace'
urlpatterns = [
    path('', views.workspace_list, name='list'),
    path('create/', views.workspace_create, name='create'),
    path('<int:workspace_id>/', views.workspace_detail, name='detail'),
    path('<int:workspace_id>/update/', views.workspace_update, name='update'),
    path('<int:workspace_id>/delete/', views.workspace_delete, name='delete'),
]
