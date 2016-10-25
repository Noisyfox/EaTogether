from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
]

if settings.DEBUG:
    urlpatterns += [url(r'^super/', include(admin.site.urls)), ]
