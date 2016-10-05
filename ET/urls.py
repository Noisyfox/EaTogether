from django.conf.urls import url, include


urlpatterns = [
    url(r"^", include('ET_Cust.urls')),
    url(r"^owner/", include('ET_Owner.urls')),
    url(r"^cour/", include('ET_Cour.urls')),
    url(r"^admin/", include('ET_Admin.urls')),
]
