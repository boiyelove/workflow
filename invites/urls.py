from django.urls import path
from . import views

app_name = 'invites'
urlpatterns = [
    path('send/<str:target_type>/<int:target_id>/', views.send_invite, name='send'),
    path('accept/<str:token>/', views.accept_invite, name='accept'),
]
