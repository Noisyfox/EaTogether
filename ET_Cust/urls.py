from django.conf.urls import url, include
from django.views.generic import TemplateView

from ET_Cust import views

urlpatterns = [
    url(r"^$", views.CustomerSearchView.as_view(), name='cust_search'),
    url(r"^login/$", views.CustomerLoginView.as_view(), name='cust_login'),
    url(r"^register/$", views.CustomerRegisterView.as_view(), name='cust_register'),
    url(r"^mainpage/$", views.CustomerMainPageView.as_view(), name='cust_main_page'),
    url(r'^restaurant/(?P<restaurant_id>[0-9]+)/group/', include([
        url(r"^$", views.CustomerRestaurantGroupView.as_view(), name='cust_restaurant_group'),
        url(r"^create/$", views.CustomerCreateGroupView.as_view(), name='cust_create_group'),
        url(r"^(?P<group_id>[0-9]+)/", include([
            url(r"^$", views.CustomerRestaurantMenuView.as_view(), name='cust_restaurant_menu'),
            url(r"^checkout/$", views.CustomerRestaurantCheckOutView.as_view(), name='cust_restaurant_checkout'),
        ])),
    ])),
    url(r"^wallet/$", views.CustomerWalletView.as_view(), name='cust_wallet'),
    url(r"^order/$", views.CustomerOrderView.as_view(), name='cust_oder'),

    # URL used to handle AJAX
    url(r"^count_people/(?P<group_id>[0-9]+)/$", views.count_people, name='count_people'),
    # url(r"^add_favorite/(?P<restaurant_id>[0-9]+)/$", views.add_favorite, name='add_favorite'),
    # url(r"^delete_favorite/(?P<restaurant_id>[0-9]+)/$", views.delete_favorite, name='delete_favorite')
]
