from django.urls import reverse_lazy

from ET.mixins import GroupRequiredMixin


class CustomerRequiredMixin(GroupRequiredMixin):
    group_required = 'customer'
    login_url = reverse_lazy('cust_login')
