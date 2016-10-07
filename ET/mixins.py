from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured
from django.utils import six


class GroupRequiredMixin(AccessMixin):
    group_required = None

    def get_required_group(self):
        if self.group_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the group_required attribute. Define {0}.group_required, or override '
                '{0}.get_required_group().'.format(self.__class__.__name__)
            )
        if isinstance(self.group_required, six.string_types):
            return self.group_required

        raise ImproperlyConfigured(
            '{0}.group_required attribute must be a string. Define {0}.group_required, or override '
            '{0}.get_required_group().'.format(self.__class__.__name__)
        )

    def in_group(self):
        group = self.get_required_group()
        return self.request.user.groups.filter(name=group).exists()

    def dispatch(self, request, *args, **kwargs):
        if not self.in_group():
            return self.handle_no_permission()
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)
