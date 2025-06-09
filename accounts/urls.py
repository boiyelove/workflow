from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('invite/', views.invite_code_view, name='invite_code'),
    path('register/<uuid:invite_code>/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('invite/create/', views.InviteUserView.as_view(), name='invite_create'),
    path('invite/list/', views.InviteListView.as_view(), name='invite_list'),
]
