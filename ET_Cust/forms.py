from ET.forms import LoginPhoneNumberForm, RegisterForm
from django import forms
from location_field.models.spatial import LocationField

GROUP = 'customer'


class CustomerRegisterForm(RegisterForm):
    group = GROUP


class CustomerLoginForm(LoginPhoneNumberForm):
    group = GROUP


class CustomerSearchRestaurantForm(forms.Form):
    restaurant = forms.CharField(max_length=30)
