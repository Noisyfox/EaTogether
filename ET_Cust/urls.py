from django.conf.urls import url
from django.views.generic import TemplateView

from ET_Cust import views

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="ET_Cust/homepage.html"), name="home"),
    url(r"^login/$", views.CustomerLoginView.as_view(), name='cust_login'),
    url(r"^register/$", views.CustomerRegisterView.as_view(), name='cust_register'),
    url(r"^search/$", views.CustomerSearchView.as_view(), name='cust_search'),
    url(r"^mainpage/$", views.CustomerMainPageView.as_view(), name='cust_main_page'),
    url(r"^restaurant/(?P<restaurant_id>[0-9]+)/group",
        TemplateView.as_view(template_name="ET_Cust/customer_restaurant_group_page.html"),
        name='cust_restaurant_group_page'),
    url(r"^creategroup/$", TemplateView.as_view(template_name="ET_Cust/customer_restaurant_menu_page.html"),
        name='home'),
]
