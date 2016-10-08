from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from ET.views import LoginView
from ET_Cust.forms import CustomerLoginForm


class CustomerLoginView(LoginView):
    form_class = CustomerLoginForm
    template_name = 'ET_Cust/login_test.html'

    def get_login_url(self):
        return reverse('cust_login')
