from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r"^customer_login/", TemplateView.as_view(template_name="ET_Cust/Customer Login.html"), name="home"),
    url(r"^customer_register/", TemplateView.as_view(template_name="ET_Cust/Customer Register.html"), name="home"),
    url(r"^customer_account_order/", TemplateView.as_view(template_name="ET_Cust/Customer Account (Order).html"), name="home"),
    url(r"^customer_account_favourite/", TemplateView.as_view(template_name="ET_Cust/Customer Account (Favourite).html"), name="home"),
    url(r"^customer_account_profile&wallet/", TemplateView.as_view(template_name="ET_Cust/Customer Account (Profile & Wallet).html"), name="home"),
    url(r"^customer_create_group/", TemplateView.as_view(template_name="ET_Cust/Customer Create Group.html"), name="home"),
    url(r"^customer_main_page/", TemplateView.as_view(template_name="ET_Cust/Customer Main Page.html"), name="home"),
    url(r"^customer_restaurant_page_group/", TemplateView.as_view(template_name="ET_Cust/Customer Restaurant Page (Group).html"), name="home"),
    url(r"^customer_restaurant_page_menu/", TemplateView.as_view(template_name="ET_Cust/Customer Restaurant Page (Menu).html"), name="home"),
    url(r"^customer_retrieve_password/", TemplateView.as_view(template_name="ET_Cust/Customer Retrieve Password.html"), name="home"),
]
