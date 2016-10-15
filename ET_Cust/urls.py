from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from ET_Cust import views

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="ET_Cust/homepage.html"), name="home"),
    url(r"^login/$", views.CustomerLoginView.as_view(), name='cust_login'),
    url(r"^register/$", views.CustomerRegisterView.as_view(), name='cust_register'),
    url(r"^groupcreate/$", views.GroupCreateView.as_view(), name='group_create'),
]
