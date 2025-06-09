from django.urls import path
from . import views

app_name = "projectflow"
urlpatterns = [
    # Project URLs
    path('', views.ProjectList.as_view(), name="project-list"),
    path('create/', views.ProjectCreate.as_view(), name="project-create"),
    path('project/<slug:slug>/', views.ProjectDetail.as_view(), name="project-detail"),
    path('project/<slug:slug>/update/', views.ProjectUpdate.as_view(), name="project-update"),
    path('project/<slug:slug>/delete/', views.ProjectDelete.as_view(), name="project-delete"),
    path('project/<slug:slug>/manage/', views.ProjectDetail.as_view(), name="project-detail-admin"),
    path('project/<slug:slug>/timeline/', views.project_timeline_view, name="project-timeline"),
    path('project/<slug:project_slug>/reorder-tasks/', views.reorder_tasks, name="reorder-tasks"),
    
    # Roadmap URLs
    path('roadmaps/', views.roadmap_list_view, name="roadmap-list"),
    path('roadmaps/<slug:slug>/', views.roadmap_detail_view, name="roadmap-detail"),
    
    # Task URLs
    path('tasks/', views.TaskList.as_view(), name="task-list"),
    path('tasks/create/', views.TaskCreate.as_view(), name="task-create"),
    path('tasks/create/<int:project_id>/', views.TaskCreate.as_view(), name="task-create-for-project"),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name="task-detail"),
    path('tasks/<int:pk>/update/', views.TaskUpdate.as_view(), name="task-update"),
    path('tasks/<int:pk>/delete/', views.TaskDelete.as_view(), name="task-delete"),
    path('tasks/<int:pk>/status/', views.update_task_status, name="task-update-status"),
    path('tasks/<int:task_id>/reorder-subtasks/', views.reorder_subtasks, name="reorder-subtasks"),
    
    # Subtask URLs
    path('subtasks/create/', views.SubTaskCreate.as_view(), name="subtask-create"),
    path('subtasks/create/<int:task_id>/', views.SubTaskCreate.as_view(), name="subtask-create-for-task"),
    path('subtasks/<int:pk>/update/', views.SubTaskUpdate.as_view(), name="subtask-update"),
    path('subtasks/<int:pk>/delete/', views.SubTaskDelete.as_view(), name="subtask-delete"),
    path('subtasks/<int:pk>/status/', views.update_subtask_status, name="subtask-update-status"),
    
    # API endpoints for Select2
    path('api/users/', views.user_search, name="user-search"),
    path('api/teams/', views.team_search, name="team-search"),
    path('api/team-members/', views.team_member_search, name="team-member-search"),
]
