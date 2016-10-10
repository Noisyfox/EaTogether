import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import TemplateView

from ET.models import Owner
from ET.views import RegisterView, LoginView
from ET_Owner.forms import OwnerRegisterForm, OwnerLoginForm, RestaurantInformationForm
from ET_Owner.mixins import RestaurantRequiredMixin, OwnerRequiredMixin


class OwnerRegisterView(RegisterView):
    form_class = OwnerRegisterForm
    template_name = 'ET_Owner/register_test.html'

    def __init__(self, **kwargs):
        super(OwnerRegisterView, self).__init__(**kwargs)
        self.success_url = reverse('owner_order_list')

    def create_user(self, form, commit=True, **kwargs):
        group = form.get_group()

        User = get_user_model()
        user = User(**kwargs)
        user.username = 'uuid_%s' % uuid.uuid4().hex[:25]
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.set_password(form.cleaned_data['password'])

        user.save()

        try:
            o = Owner(user=user)
            o.phone_number = form.cleaned_data['phone_number']
            o.save()
        except Exception:
            user.delete()
            raise

        user.groups.add(Group.objects.get(name__exact=group))
        user.save()

        return user

    def get_register_url(self):
        return reverse('owner_register')


class OwnerLoginView(LoginView):
    form_class = OwnerLoginForm
    template_name = 'ET_Owner/login_test.html'

    def __init__(self, **kwargs):
        super(OwnerLoginView, self).__init__(**kwargs)
        self.success_url = reverse('owner_order_list')

    def get_login_url(self):
        return reverse('owner_login')

    def get_signup_url(self):
        return reverse('owner_register')


class OwnerOrderListView(RestaurantRequiredMixin, TemplateView):
    template_name = 'ET_Cust/homepage.html'


class OwnerRestaurantCreateView(OwnerRequiredMixin, FormView):
    form_class = RestaurantInformationForm
    template_name = 'ET_Owner/restaurant_information_test.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(OwnerRestaurantCreateView, self).get_initial()

        initial['general'] = {'location': '0,0'}

        return initial
