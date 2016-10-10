from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from ET.mixins import GroupRequiredMixin


class OwnerRequiredMixin(GroupRequiredMixin):
    group_required = 'owner'

    def __init__(self):
        super(OwnerRequiredMixin, self).__init__()
        self.login_url = reverse('owner_login')


class RestaurantRequiredMixin(OwnerRequiredMixin):

    def __init__(self):
        super(RestaurantRequiredMixin, self).__init__()
        self.restaurant_create_url = reverse('owner_edit_restaurant')

    def dispatch(self, request, *args, **kwargs):
        if not self.in_group():
            return self.handle_no_permission()

        # check restaurant
        try:
            self.request.user.owner.restaurant
        except ObjectDoesNotExist:
            self.login_url = self.restaurant_create_url
            return self.handle_no_permission()

        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)
