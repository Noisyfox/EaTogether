from ET.forms import LoginPhoneNumberForm, RegisterForm

GROUP = 'customer'


class CustomerRegisterForm(RegisterForm):
    group = GROUP


class CustomerLoginForm(LoginPhoneNumberForm):
    group = GROUP
