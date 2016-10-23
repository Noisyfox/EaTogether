import uuid

from crispy_forms.layout import Submit
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as UserGroup
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
from django.views.generic import FormView, CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from ET.forms import FormHelper
from ET.models import Customer, Group, Restaurant, Food
from ET.views import LoginView, RegisterView
from ET_Cust.forms import CustomerLoginForm, CustomerRegisterForm, CustomerSearchRestaurantForm, \
    CustomerSearchAddressForm
from ET_Cust.mixins import CustomerRequiredMixin
from django.http import HttpResponse


class CustomerRegisterView(RegisterView):
    form_class = CustomerRegisterForm
    template_name = 'ET_Cust/register_test.html'
    success_url = reverse_lazy('cust_search')

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
            user.groups.add(Group.objects.get(name__exact=group))
        except Exception:
            user.delete()
            raise

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


class CustomerSearchView(FormView):
    form_class = CustomerSearchAddressForm
    template_name = 'ET_Cust/customer_search.html'
    success_url = reverse_lazy('cust_main_page')

    def form_valid(self, form):
        self.request.session['address'] = form.cleaned_data['address']
        self.request.session['location'] = form.cleaned_data['location']
        return super(CustomerSearchView, self).form_valid(form)


class CustomerMainPageView(ListView):
    template_name = 'ET_Cust/customer_main_page.html'
    model = Restaurant
    context_object_name = 'restaurant_list'

    def get_context_data(self, **kwargs):
        context = super(CustomerMainPageView, self).get_context_data(**kwargs)
        form = CustomerSearchRestaurantForm()
        context['form'] = form
        context['address'] = self.request.session['address']
        return context

    def post(self, request, *args, **kwargs):
        form = CustomerSearchRestaurantForm(request.POST)
        if form.is_valid():
            self.queryset = self.queryset.filter(name__contains=form.cleaned_data['restaurant'])
            return self.get(self, request, *args, **kwargs)
        else:
            return self.get(self, request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        location_search = GEOSGeometry(self.request.session['location'], srid=4326)
        self.queryset = Restaurant.objects.annotate(distance=Distance('location', location_search)).order_by('distance')
        return super(CustomerMainPageView, self).dispatch(request, *args, **kwargs)


class CustomerRestaurantGroupView(ListView):
    template_name = 'ET_Cust/customer_restaurant_group_page.html'
    model = Group
    context_object_name = 'group_list'

    def get_context_data(self, **kwargs):
        context = super(CustomerRestaurantGroupView, self).get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        context['address'] = self.request.session['address']
        return context


class CustomerCreateGroupView(CreateView):
    template_name = 'ET_Cust/customer_create_group.html'
    model = Group
    fields = ['destination', 'location', 'group_time']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Create'))
        return form

    def form_valid(self, form, **kwargs):
        form.instance.create_time = timezone.now()
        form.instance.restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        return super(CustomerCreateGroupView, self).form_valid(form)


class CustomerRestaurantMenuView(ListView):
    template_name = 'ET_Cust/customer_restaurant_menu_page.html'
    model = Food
    context_object_name = 'food_list'

    def get_context_data(self, **kwargs):
        context = super(CustomerRestaurantMenuView, self).get_context_data(**kwargs)
        context['food_list'] = context['food_list'].filter(restaurant__id=self.kwargs['restaurant_id'])
        context['restaurant'] = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        # context['address'] = self.request.session['address']
        return context
