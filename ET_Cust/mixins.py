from django.urls import reverse

from ET.mixins import GroupRequiredMixin


class CustomerRequiredMixin(GroupRequiredMixin):
    group_required = 'customer'

    def __init__(self):
        super(CustomerRequiredMixin, self).__init__()
        self.login_url = reverse('cust_login')
