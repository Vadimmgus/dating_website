
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_url

from .yasg import urlpatterns as doc_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('meeting_website.urls_api')),
] + doc_url
