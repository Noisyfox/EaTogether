from django.urls import reverse

from ET.mixins import GroupRequiredMixin


class CustomerRequiredMixin(GroupRequiredMixin):
    group_required = 'customer'
    login_url = reverse('cust_login')
