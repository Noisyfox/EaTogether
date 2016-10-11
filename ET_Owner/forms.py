from django import forms
from django.utils.translation import ugettext_lazy as _
from betterforms.multiform import MultiForm

from ET.forms import LoginPhoneNumberForm, RegisterForm
from location_field.forms.spatial import LocationField

GROUP = 'owner'


class OwnerRegisterForm(RegisterForm):
    group = GROUP


class OwnerLoginForm(LoginPhoneNumberForm):
    group = GROUP


class RestaurantGeneralInformationForm(forms.Form):
    name = forms.CharField(label=_('Restaurant Name'), strip=True, max_length=30)
    contact_name = forms.CharField(label=_('Contact Name'), strip=True, max_length=30)
    contact_number = forms.CharField(label=_('Contact Number'), strip=True, max_length=10)
    introduction = forms.CharField(widget=forms.Textarea, label=_('Restaurant Introduction'), strip=True,
                                   max_length=200)

    address = forms.CharField(label=_('Address'), strip=True, max_length=128)

    location = LocationField(address_field='address', zoom=13)
    logo = forms.ImageField(label=_('Logo'))


class RestaurantValidInformationForm(forms.Form):
    name = forms.CharField(label=_('Id'), strip=True, max_length=30)
    id_number = forms.CharField(label=_('Id Number'), strip=True, max_length=30)


class RestaurantInformationForm(MultiForm):
    form_classes = {
        'general': RestaurantGeneralInformationForm,
        'valid': RestaurantValidInformationForm,
    }
