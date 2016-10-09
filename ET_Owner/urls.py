from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r"^login/$", TemplateView.as_view(template_name="ET_Owner/owner_login.html"), name="owner_login"),
]
