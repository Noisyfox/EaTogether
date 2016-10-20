from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r"^customer_login/", TemplateView.as_view(template_name="ET_Cust/Customer Login.html"), name="customer login"),
    url(r"^customer_register/", TemplateView.as_view(template_name="ET_Cust/Customer Register.html"), name="customer register"),
    url(r"^customer_account_order/", TemplateView.as_view(template_name="ET_Cust/Customer Account (Order).html"), name="customer account order"),
    url(r"^customer_account_favourite/", TemplateView.as_view(template_name="ET_Cust/Customer Account (Favourite).html"), name="customer account favourite"),
    url(r"^customer_account_profile&wallet/", TemplateView.as_view(template_name="ET_Cust/Customer Account (Profile & Wallet).html"), name="customer account profile&wallet"),
    url(r"^customer_create_group/", TemplateView.as_view(template_name="ET_Cust/Customer Create Group.html"), name="customer create group"),
    url(r"^customer_main_page/", TemplateView.as_view(template_name="ET_Cust/Customer Main Page.html"), name="customer main group"),
    url(r"^customer_restaurant_page_group/", TemplateView.as_view(template_name="ET_Cust/Customer Restaurant Page (Group).html"), name="customer restaurant page group"),
    url(r"^customer_restaurant_page_menu/", TemplateView.as_view(template_name="ET_Cust/Customer Restaurant Page (Menu).html"), name="customer restaurant page menu"),
    url(r"^customer_retrieve_password/", TemplateView.as_view(template_name="ET_Cust/Customer Retrieve Password.html"), name="customer retrieve password"),
]
