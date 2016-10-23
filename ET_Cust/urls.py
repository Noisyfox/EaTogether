from django.conf.urls import url
from django.views.generic import TemplateView

from ET_Cust import views

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="ET_Cust/homepage.html"), name="home"),
    url(r"^login/$", views.CustomerLoginView.as_view(), name='cust_login'),
    url(r"^register/$", views.CustomerRegisterView.as_view(), name='cust_register'),
    url(r"^search/$", views.CustomerSearchView.as_view(), name='cust_search'),
    url(r"^mainpage/$", views.CustomerMainPageView.as_view(), name='cust_main_page'),
    url(r"^restaurant/(?P<restaurant_id>[0-9]+)/group/$",
        views.CustomerRestaurantGroupView.as_view(template_name="ET_Cust/customer_restaurant_group_page.html"),
        name='cust_restaurant_group'),
    url(r"^restaurant/(?P<restaurant_id>[0-9]+)/group/create/$",
        views.CustomerCreateGroupView.as_view(template_name="ET_Cust/customer_create_group.html"),
        name='cust_create_group'),
    url(r"^restaurant/(?P<restaurant_id>[0-9]+)/group/(?P<group_id>[0-9]+)/$",
        views.CustomerRestaurantMenuView.as_view(template_name="ET_cust/customer_restaurant_menu_page.html"),
        name='cust_restaurant_menu')
]
