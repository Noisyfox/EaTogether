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
        url(r'^count/$', views.count_current_group, name='count_current_group'),
    ])),
    url(r"^wallet/$", views.CustomerWalletView.as_view(), name='cust_wallet'),
    url(r"^order/$", views.CustomerOrderView.as_view(), name='cust_order'),
    url(r"^favorite/$", views.CustomerFavoriteView.as_view(), name='cust_favorite'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),

    # URL used to handle AJAX
    url(r"^group/(?P<group_id>[0-9]+)/count$", views.count_people, name='count_people'),
    url(r"^add_favorite/(?P<restaurant_id>[0-9]+)/$", views.AddFavoriteView.as_view(), name='add_favorite'),
    url(r"^delete_favorite/(?P<restaurant_id>[0-9]+)/$", views.DeleteFavoriteView.as_view(), name='delete_favorite'),
    url(r"^logout/", TemplateView.as_view(template_name="ET_Cust/customer_logout.html"), name="cust_logout"),
]
