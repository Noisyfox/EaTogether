from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Fieldset
from django import forms
from django.utils.translation import ugettext_lazy as _

from ET.forms import LoginPhoneNumberForm, RegisterForm, FormMixin
from ET.models import Restaurant, Food

GROUP = 'owner'


class OwnerRegisterForm(RegisterForm):
    group = GROUP


class OwnerLoginForm(LoginPhoneNumberForm):
    group = GROUP


class RestaurantEditForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'contact_name', 'contact_number', 'introduction', 'address', 'location', 'logo',
                  'id_number', 'id_photo', 'business_license']
        labels = {
            'name': _('Restaurant Name'),
            'contact_name': _('Contact Name'),
            'contact_number': _('Contact Number'),
            'introduction': _('Introduction'),
            'address': _('Address'),
            'location': _('Location'),
            'logo': _('Logo'),
        }

    def __init__(self, *args, **kwargs):
        super(RestaurantEditForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'restaurant_form'

        self.helper.layout = Layout(
            Fieldset(
                'General Information',
                'name', 'contact_name', 'contact_number', 'introduction', 'address', 'location', 'logo',
            ),
            Fieldset(
                'Sufficient Valid Information',
                'id_number', 'id_photo', 'business_license'
            ),
            FormActions(
                Submit('save', 'Save')
            )
        )


class FoodEditForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'introduction', 'picture', 'price']

    def __init__(self, *args, **kwargs):
        super(FoodEditForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'food_form'

        self.helper.add_input(Submit('save', 'Save'))
