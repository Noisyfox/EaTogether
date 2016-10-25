from django.shortcuts import render
from django.urls import reverse_lazy

from ET.views import LoginView
from ET_Cour.forms import CourierLoginForm


class CourierLoginView(LoginView):
    form_class = CourierLoginForm
    template_name = 'ET_Cour/login.html'
    success_url = reverse_lazy('cour_order')

    def get_login_url(self):
        return reverse_lazy('cour_login')
