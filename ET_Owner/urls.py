from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from ET_Owner import views

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="ET_Cust/homepage.html"), name="home"),
    url(r"^login/$", views.OwnerLoginView.as_view(), name='owner_login'),
    url(r"^register/$", views.OwnerRegisterView.as_view(), name='owner_register'),
]
