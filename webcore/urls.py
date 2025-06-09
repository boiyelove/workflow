from django.urls import path
from . import views

app_name = 'webcore'
urlpatterns = [
    path('', views.home, name='home'),
]
