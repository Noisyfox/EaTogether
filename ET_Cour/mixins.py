from ET.mixins import GroupRequiredMixin


class CourierRequiredMixin(GroupRequiredMixin):
    group_required = 'courier'
    login_url = ''
