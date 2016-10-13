from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r"^login/$", TemplateView.as_view(template_name="ET_Owner/owner_login.html"), name="owner_login"),
    url(r"^register/$", TemplateView.as_view(template_name="ET_Owner/owner_register.html"), name="owner_register"),
    url(r"^editfood/$", TemplateView.as_view(template_name="ET_Owner/owner_edit_food.html"), name="owner_edit_food"),
    url(r"^retrieve/$", TemplateView.as_view(template_name="ET_Owner/owner_password_retrieve.html"), name="owner_retrieve_password"),
    url(r"^myrestaurant/$", TemplateView.as_view(template_name="ET_Owner/owner_my_restaurant.html.html"), name="owner_restaurant_info"),
]
