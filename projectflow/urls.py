from django.urls import path
from . import views

app_name = 'projectflow'
urlpatterns = [
    # Project URLs
    path('', views.project_list, name="project-list"),
    path('create/', views.project_create, name="project-create"),
    path('project/<slug:slug>/', views.project_detail, name="project-detail"),
    path('project/<slug:slug>/update/', views.project_update, name="project-update"),
    path('project/<slug:slug>/delete/', views.project_delete, name="project-delete"),
    path('project/<slug:slug>/timeline/', views.project_timeline_view, name="project-timeline"),
    path('project/<slug:project_slug>/reorder-tasks/', views.reorder_tasks, name="reorder-tasks"),
    
    # Roadmap URLs
    path('roadmaps/', views.roadmap_list_view, name="roadmap-list"),
    path('roadmaps/<slug:slug>/', views.roadmap_detail_view, name="roadmap-detail"),
    
    # Task URLs
    path('tasks/', views.task_list, name="task-list"),
    path('tasks/create/', views.task_create, name="task-create"),
    path('tasks/create/<int:project_id>/', views.task_create, name="task-create-for-project"),
    path('tasks/<int:pk>/', views.task_detail, name="task-detail"),
    path('tasks/<int:pk>/update/', views.task_update, name="task-update"),
    path('tasks/<int:pk>/delete/', views.task_delete, name="task-delete"),
    path('tasks/<int:pk>/status/', views.update_task_status, name="task-update-status"),
    path('tasks/<int:task_id>/reorder-subtasks/', views.reorder_subtasks, name="reorder-subtasks"),
    
    # Subtask URLs
    path('subtasks/create/', views.subtask_create, name="subtask-create"),
    path('subtasks/create/<int:task_id>/', views.subtask_create, name="subtask-create-for-task"),
    path('subtasks/<int:pk>/update/', views.subtask_update, name="subtask-update"),
    path('subtasks/<int:pk>/delete/', views.subtask_delete, name="subtask-delete"),
    path('subtasks/<int:pk>/status/', views.update_subtask_status, name="subtask-update-status"),
]
