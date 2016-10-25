from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from ET.views import LoginView
from ET_Cour.forms import CourierLoginForm
from ET_Cour.mixins import CourierRequiredMixin


class CourierLoginView(LoginView):
    form_class = CourierLoginForm
    template_name = 'ET_Cour/login.html'
    success_url = reverse_lazy('cour_order')

    def get_login_url(self):
        return reverse_lazy('cour_login')


class CourierOrderListView(CourierRequiredMixin, ListView):
    template_name = 'ET_Cour/order.html'
    context_object_name = 'orders'
    allow_empty = True

    def get_queryset(self):
        return self.request.user.courier.grouporder_set.order_by('-delivery_start_time')
