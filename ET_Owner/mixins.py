from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy

from ET.mixins import GroupRequiredMixin


class OwnerRequiredMixin(GroupRequiredMixin):
    group_required = 'owner'
    login_url = reverse_lazy('owner_login')


class RestaurantRequiredMixin(OwnerRequiredMixin):
    restaurant_create_url = reverse_lazy('owner_edit_restaurant')

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
