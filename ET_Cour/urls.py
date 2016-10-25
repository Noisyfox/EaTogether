from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from ET_Cour import views

urlpatterns = [
    url(r"^login/$", views.CourierLoginView.as_view(), name='cour_login'),
    url(r"^order/", include([
        url(r"^$", views.CourierOrderListView.as_view(), name='cour_order'),
        url('^(?P<order_id>[0-9]+)/', include([
            url(r"^$", TemplateView.as_view(template_name="ET_Cour/detail.html"), name='cour_detail'),
        ])),
    ])),
]
