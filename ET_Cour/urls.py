from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from ET_Cour import views


urlpatterns = [
    url(r"^login/$", TemplateView.as_view(template_name="ET_Cour/login.html")),
    url(r"^detail/$", TemplateView.as_view(template_name="ET_Cour/detail.html")),
    url(r"^order/$", TemplateView.as_view(template_name="ET_Cour/order.html")),
]
