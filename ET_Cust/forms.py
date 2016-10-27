from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.layout import Submit, Layout

from ET.forms import LoginPhoneNumberForm, RegisterForm, FormMixin
from django import forms
from location_field.forms.spatial import LocationField

GROUP = 'customer'


class CustomerRegisterForm(RegisterForm):
    group = GROUP


class CustomerLoginForm(LoginPhoneNumberForm):
    group = GROUP


# The form which customers use to search the restaurant near the address input.
class CustomerSearchAddressForm(FormMixin, forms.Form):
    address = forms.CharField(max_length=255)
    location = LocationField(address_field='address', zoom=13)

    def __init__(self, *args, **kwargs):
        super(CustomerSearchAddressForm, self).__init__(*args, **kwargs)

        self.helper.add_input(Submit('search', 'Search'))


# The form which customers use to search the certain restaurant.
class CustomerSearchRestaurantForm(FormMixin, forms.Form):
    restaurant = forms.CharField(max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        super(CustomerSearchRestaurantForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            FieldWithButtons('restaurant', Submit('search', 'Search'))
        )
