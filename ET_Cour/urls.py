from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from ET_Cour import views

urlpatterns = [
    url(r"^login/$", views.CourierLoginView.as_view(), name='cour_login'),
    url(r"^detail/$", TemplateView.as_view(template_name="ET_Cour/detail.html"), name='cour_detail'),
    url(r"^order/$", TemplateView.as_view(template_name="ET_Cour/order.html"), name='cour_order'),
]
