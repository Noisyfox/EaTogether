from django import forms
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False,
    )
    user = None
    group = None
    identifier_field = None
    authentication_fail_message = _('The information you provided are not correct.')

    def clean(self):
        if self._errors:
            return

        user = auth.authenticate(**self.user_credentials())
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_('This account is inactive.'))
        else:
            raise forms.ValidationError(self.authentication_fail_message)

        return self.cleaned_data

    def get_group(self):
        if self.group is None:
            raise ImproperlyConfigured(
                '{0} is missing the group attribute. Define {0}.group.'.format(self.__class__.__name__)
            )
        if isinstance(self.group, six.string_types):
            return self.group

        raise ImproperlyConfigured(
            '{0}.group_required attribute must be a string. Define {0}.group_required, or override '
            '{0}.get_required_group().'.format(self.__class__.__name__)
        )

    def user_credentials(self):
        if self.identifier_field is None:
            raise ImproperlyConfigured(
                '{0} is missing the identifier_field attribute. Define {0}.identifier_field. or override '
                '{0}.user_credentials().'.format(self.__class__.__name__)
            )

        return {
            "username": self.cleaned_data[self.identifier_field],
            "password": self.cleaned_data["password"],
            "group": self.get_group()
        }


class LoginPhoneNumberForm(LoginForm):
    phone_number = forms.CharField(label=_('Phone Number'), max_length=12)
    authentication_fail_message = _("The phone number and/or password you specified are not correct.")
    field_order = ['phone_number', 'password', 'remember']
    identifier_field = 'phone_number'
