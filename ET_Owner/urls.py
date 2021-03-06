from django.conf.urls import url, include
from django.views.generic import RedirectView

from django.views.generic import TemplateView

from django.contrib import admin

from ET_Owner import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='owner_order_list', permanent=False), name='owner'),
    url(r"^order/", include([
        url(r"^$", views.OrderListView.as_view(), name="owner_order_list"),
        url('^(?P<order_id>[0-9]+)/', include([
            url(r"^accept/$", views.OrderAcceptView.as_view(), name="owner_order_accept"),
            url(r"^delivery/$", views.OrderDeliveryView.as_view(), name="owner_order_delivery"),
        ])),
    ])),
    url(r"^login/$", views.OwnerLoginView.as_view(), name='owner_login'),
    url(r"^register/$", views.OwnerRegisterView.as_view(), name='owner_register'),
    url(r"^restaurant/$", views.OwnerRestaurantEditView.as_view(), name='owner_edit_restaurant'),
    url(r"^menu/$", views.OwnerMenuView.as_view(), name='owner_menu'),
    url(r"^service/$", views.ServiceInfoUpdateView.as_view(), name='owner_service_info_edit'),
    url(r"^food/", include([
        url("^new/$", views.OwnerFoodCreateView.as_view(), name='owner_create_food'),
        url("^(?P<pk>[0-9]+)/$", views.OwnerFoodEditView.as_view(), name='owner_edit_food'),
    ])),
    url(r'^courier/', include([
        url('^$', views.OwnerCourierView.as_view(), name='owner_courier'),
        url('^new/$', views.OwnerCourierCreateView.as_view(), name='owner_create_courier'),
        url('^(?P<pk>[0-9]+)/', include([
            url('^$', views.OwnerCourierEditView.as_view(), name='owner_edit_courier'),
            url('^delete/$', views.AssignmentDeleteView.as_view(), name='owner_delete_courier'),
        ])),
    ])),
    url(r"^wallet/$", views.WalletView.as_view(), name='owner_wallet'),
]
