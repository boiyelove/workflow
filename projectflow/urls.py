from django.urls import urls
from . import views

app_name = "projectflow"
urlpatterns = [
	url(r'^$'),
	url(r'^projects/$', views.ProjectList.as_view(), name="project-detail"),
	url(r'^projects/manage/$', views.ProjectList.as_view(), name="project-detail"),
	url(r'^(?P<project_slug>[\w+]-)/manage/$', views.ProjectDetail.as_view(), name="project-detail-admin"),
	url(r'^(?P<project_slug>[\w+]-)/$', views.ProjectDetail.as_view(), name="project-detail"),
	
	]