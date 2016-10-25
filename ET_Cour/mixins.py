from django.urls import reverse_lazy

from ET.mixins import GroupRequiredMixin


class CourierRequiredMixin(GroupRequiredMixin):
    group_required = 'courier'
    login_url = reverse_lazy('cour_login')
