from captcha.fields import ReCaptchaField
from crispy_forms import helper
from crispy_forms.layout import Submit, Hidden
from django import forms
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from ET.models import Customer, Owner


class FormHelper(helper.FormHelper):
    include_media = False


class FormMixin(object):
    def __init__(self, *args, **kwargs):
        redirect_field_name = kwargs.pop('redirect_field_name', None)
        redirect_field_value = kwargs.pop('redirect_field_value', None)

        super(FormMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        if redirect_field_name:
            self.helper.add_input(Hidden(redirect_field_name, redirect_field_value))


class RegisterForm(FormMixin, forms.Form):
    first_name = forms.CharField(
        label=_('Given Name'),
        max_length=20,
        widget=forms.TextInput(),
        strip=True,
        required=True
    )
    last_name = forms.CharField(
        label=_('Family Name'),
        max_length=20,
        widget=forms.TextInput(),
        strip=True,
        required=True
    )
    phone_number = forms.CharField(
        label=_('Phone Number'),
        max_length=12,
        strip=True,
        required=True
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )
    captcha = ReCaptchaField(
        label=_("Turin Test"),
    )
    group = None

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('register', 'Register'))

    def clean_phone_number(self):
        g = self.get_group()
        phone = self.cleaned_data['phone_number']
        if g == 'customer':
            qs = Customer.objects.filter(phone_number__iexact=phone)
        elif g == 'owner':
            qs = Owner.objects.filter(phone_number__iexact=phone)
        else:
            return self.cleaned_data['phone_number']

        if not qs.exists():
            return self.cleaned_data["phone_number"]
        raise forms.ValidationError(_("This phone number is already taken. Please input another."))

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
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


class LoginForm(FormMixin, forms.Form):
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False,
    )
    captcha = ReCaptchaField(
        label=_("Turin Test"),
    )
    user = None
    group = None
    identifier_field = None
    authentication_fail_message = _('The information you provided are not correct.')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('login', 'Login'))

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
    phone_number = forms.CharField(label=_('Phone Number'), strip=True, max_length=12)
    authentication_fail_message = _("The phone number and/or password you specified are not correct.")
    field_order = ['phone_number', 'password', 'captcha', 'remember']
    identifier_field = 'phone_number'
