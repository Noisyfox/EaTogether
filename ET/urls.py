from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static


urlpatterns = [
    url(r"^", include('ET_Cust.urls')),
    url(r"^owner/", include('ET_Owner.urls')),
    url(r"^cour/", include('ET_Cour.urls')),
    url(r"^admin/", include('ET_Admin.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
