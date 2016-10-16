import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from ET.models import Customer, Group, Restaurant
from ET.views import LoginView, RegisterView
from ET_Cust.forms import CustomerLoginForm, CustomerRegisterForm, CustomerSearchRestaurantForm
from ET_Cust.mixins import CustomerRequiredMixin
from django.http import HttpResponse



class CustomerRegisterView(RegisterView):
    form_class = CustomerRegisterForm
    template_name = 'ET_Cust/register_test.html'

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
            c = Customer(user=user)
            c.phone_number = form.cleaned_data['phone_number']
            c.save()
        except Exception:
            user.delete()
            raise

        user.groups.add(Group.objects.get(name__exact=group))
        user.save()

        return user

    def get_register_url(self):
        return reverse_lazy('cust_register')


class CustomerLoginView(LoginView):
    form_class = CustomerLoginForm
    template_name = 'ET_Cust/login_test.html'

    def get_login_url(self):
        return reverse_lazy('cust_login')

    def get_signup_url(self):
        return reverse_lazy('cust_register')


class CustomerMainPageView(ListView, CustomerRequiredMixin):
    template_name = 'ET_Cust/customer_main_page.html'
    model = Restaurant
    context_object_name = 'restaurant_list'

    def get_context_data(self, **kwargs):
        context = super(CustomerMainPageView, self).get_context_data(**kwargs)
        form = CustomerSearchRestaurantForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CustomerSearchRestaurantForm(request.POST)
        if form.is_valid():
            self.queryset = Restaurant.objects.filter(name__contains=form.cleaned_data['restaurant'])
            return self.get(self, request, *args, **kwargs)
        else:
            return self.get(self, request, *args, **kwargs)










