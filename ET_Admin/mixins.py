from ET.mixins import GroupRequiredMixin


class AdminRequiredMixin(GroupRequiredMixin):
    group_required = 'admin'
    login_url = ''
