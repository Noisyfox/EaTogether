from ET.forms import LoginPhoneNumberForm, RegisterForm
from django import forms
from location_field.forms.spatial import LocationField


GROUP = 'customer'


class CustomerRegisterForm(RegisterForm):
    group = GROUP


class CustomerLoginForm(LoginPhoneNumberForm):
    group = GROUP


# The form which customers use to search the restaurant near the address input.
class CustomerSearchAddressForm(forms.Form):
    address = forms.CharField(max_length=255)
    location = LocationField(address_field='address', zoom=13)


# The form which customers use to search the certain restaurant.
class CustomerSearchRestaurantForm(forms.Form):
    restaurant = forms.CharField(max_length=30)
