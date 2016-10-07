from django import forms
from django.utils.translation import ugettext_lazy as _

from ET.forms import LoginForm


class AdminLoginForm(LoginForm):
    username = forms.CharField(label=_("Username"), max_length=30)
    authentication_fail_message = _("The username and/or password you specified are not correct.")
    field_order = ["username", "password", "remember"]
    group = 'admin'
    identifier_field = 'username'
