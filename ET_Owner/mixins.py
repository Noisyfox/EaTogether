from ET.mixins import GroupRequiredMixin


class OwnerRequiredMixin(GroupRequiredMixin):
    group_required = 'owner'
    login_url = ''
