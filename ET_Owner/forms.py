from django import forms
from django.utils.translation import ugettext_lazy as _
from betterforms.multiform import MultiForm, MultiModelForm

from ET.forms import LoginPhoneNumberForm, RegisterForm
from ET.models import Restaurant, ValidationInformation

GROUP = 'owner'


class OwnerRegisterForm(RegisterForm):
    group = GROUP


class OwnerLoginForm(LoginPhoneNumberForm):
    group = GROUP


class RestaurantGeneralInformationForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'contact_name', 'contact_number', 'introduction', 'address', 'location', 'logo']
        labels = {
            'name': _('Restaurant Name'),
            'contact_name': _('Contact Name'),
            'contact_number': _('Contact Number'),
            'introduction': _('Introduction'),
            'address': _('Address'),
            'location': _('Location'),
            'logo': _('Logo'),
        }


class RestaurantValidInformationForm(forms.ModelForm):
    class Meta:
        model = ValidationInformation
        fields = ['id_number', 'id_photo', 'business_license']


class RestaurantInformationForm(MultiModelForm):
    form_classes = {
        'general': RestaurantGeneralInformationForm,
        'valid': RestaurantValidInformationForm,
    }
