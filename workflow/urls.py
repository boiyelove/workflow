from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from webcore.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='home'),
    path('accounts/', include('accounts.urls')),
    path('projects/', include('projectflow.urls')),
    path('teams/', include('teamflow.urls')),
    path('workspaces/', include('workspace.urls')),
    path('invites/', include('invites.urls')),
    path('support/', include('support.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
