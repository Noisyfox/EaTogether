from ET.forms import LoginPhoneNumberForm, RegisterForm

GROUP = 'owner'


class OwnerRegisterForm(RegisterForm):
    group = GROUP


class OwnerLoginForm(LoginPhoneNumberForm):
    group = GROUP
