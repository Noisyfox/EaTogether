from django.conf import settings
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.views.generic import FormView


class LoginView(FormView):
    # template_name = 'account/login.html'
    # form_class = None
    form_kwargs = {}
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        ctx = super(LoginView, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name,
                                                          self.request.GET.get(redirect_field_name, "")),
            "login_url": self.get_login_url(),
            "password_reset_url": self.get_password_reset_url(),
            "signup_url": self.get_signup_url(),
        })
        return ctx

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_valid(self, form):
        self.login_user(form)
        success_url = self.get_success_url()
        if not success_url:
            raise ImproperlyConfigured(
                '{0}.get_success_url() returns None. Override {0}.get_success_url().'.format(self.__class__.__name__)
            )

        return redirect(success_url)

    def get_success_url(self, **kwargs):
        redirect_field_name = self.get_redirect_field_name()
        next_url = self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name))
        return next_url

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def login_user(self, form):
        auth.login(self.request, form.user)
        expiry = settings.ET_REMEMBER_ME_EXPIRY if form.cleaned_data.get("remember") else 0
        self.request.session.set_expiry(expiry)

    def get_login_url(self):
        raise NotImplementedError

    def get_password_reset_url(self):
        return None

    def get_signup_url(self):
        return None
