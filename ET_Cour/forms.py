from django import forms
from django.utils.translation import ugettext_lazy as _

from ET.forms import LoginPhoneNumberForm


class CourierLoginForm(LoginPhoneNumberForm):
    courier_id = forms.CharField(label=_('Courier Id'), max_length=30)
    authentication_fail_message = _("The phone number, courier id and/or password you specified are not correct.")
    field_order = ['phone_number', 'courier_id', 'password', 'remember']
    group = 'courier'

    def __init__(self, *args, **kwargs):
        super(CourierLoginForm, self).__init__(*args, **kwargs)
        self.phone_number.label = _('Owner Phone Number')

    def user_credentials(self):
        credentials = super().user_credentials()
        credentials.update({'courier_id': self.cleaned_data['courier_id']})

        return credentials
