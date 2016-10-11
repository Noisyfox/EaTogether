import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from ET.models import Owner
from ET.views import RegisterView, LoginView
from ET_Owner.forms import OwnerRegisterForm, OwnerLoginForm, RestaurantInformationForm, RestaurantValidInformationForm
from ET_Owner.mixins import RestaurantRequiredMixin, OwnerRequiredMixin


class OwnerRegisterView(RegisterView):
    form_class = OwnerRegisterForm
    template_name = 'ET_Owner/register_test.html'
    success_url = reverse_lazy('owner_order_list')

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
        return reverse_lazy('owner_register')


class OwnerLoginView(LoginView):
    form_class = OwnerLoginForm
    template_name = 'ET_Owner/login_test.html'
    success_url = reverse_lazy('owner_order_list')

    def get_login_url(self):
        return reverse_lazy('owner_login')

    def get_signup_url(self):
        return reverse_lazy('owner_register')


class OwnerOrderListView(RestaurantRequiredMixin, TemplateView):
    template_name = 'ET_Cust/homepage.html'


class OwnerRestaurantInformationView(OwnerRequiredMixin, UpdateView):
    form_class = RestaurantInformationForm
    template_name = 'ET_Owner/restaurant_information_test.html'
    success_url = reverse_lazy('owner_restaurant')

    def get_object(self, queryset=None):
        try:
            return self.request.user.owner.restaurant
        except ObjectDoesNotExist:
            return None

    def get_form_kwargs(self):
        kwargs = super(OwnerRestaurantInformationView, self).get_form_kwargs()
        if self.object:
            kwargs.update(instance={
                'general': self.object,
                'valid': self.object.validationinformation,
            })

        return kwargs

    def form_valid(self, form):
        if not self.object:
            new_obj = form.save(commit=False)
            restaurant = new_obj['general']
            valid = new_obj['valid']
            restaurant.owner = self.request.user.owner
            restaurant.save()
            try:
                valid.restaurant = restaurant
                valid.save()
            except Exception:
                restaurant.delete()
                raise

            self.object = new_obj

            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(OwnerRestaurantInformationView, self).form_valid(form)
