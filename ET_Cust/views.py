import uuid
from crispy_forms.layout import Submit
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as UserGroup
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.template import RequestContext
from django.views.generic import View, TemplateView, DetailView
from django.views.generic import FormView, CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from ET.forms import FormHelper
from ET.models import Customer, Group, Restaurant, Food, OrderFood, PersonalOrder
from ET.views import LoginView, RegisterView
from ET_Cust.forms import CustomerLoginForm, CustomerRegisterForm, CustomerSearchRestaurantForm, \
    CustomerSearchAddressForm
from ET_Cust.mixins import CustomerRequiredMixin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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
            user.groups.add(UserGroup.objects.get(name__exact=group))
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
    success_url = reverse_lazy('cust_search')

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


class CustomerRestaurantGroupView(CustomerRequiredMixin, ListView):
    template_name = 'ET_Cust/customer_restaurant_group_page.html'
    model = Group
    context_object_name = 'group_list'

    def get_context_data(self, **kwargs):
        context = super(CustomerRestaurantGroupView, self).get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        context['address'] = self.request.session['address']
        return context

    def get_queryset(self, **kwargs):
        queryset = super(CustomerRestaurantGroupView, self).get_queryset(**kwargs)
        queryset = queryset.filter(restaurant=self.kwargs['restaurant_id']).filter(status='G')
        return queryset


class CustomerCreateGroupView(CustomerRequiredMixin, CreateView):
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


class CustomerRestaurantMenuView(CustomerRequiredMixin, ListView):
    template_name = 'ET_Cust/customer_restaurant_menu_page_test.html'
    model = Food
    context_object_name = 'food_list'

    def get_context_data(self, **kwargs):
        context = super(CustomerRestaurantMenuView, self).get_context_data(**kwargs)
        context['food_list'] = context['food_list'].filter(restaurant__id=self.kwargs['restaurant_id'])
        context['restaurant'] = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        context['group'] = self.kwargs['group_id']
        # context['address'] = self.request.session['address']
        return context


class CustomerRestaurantCheckOutView(CustomerRequiredMixin, ListView):
    template_name = 'ET_Cust/customer_restaurant_checkout_page.html'
    model = OrderFood
    context_object_name = 'orderfood_list'
    frozen_price = 0
    personal_order_id = 0

    def post(self, request, *args, **kwargs):
        k = int(request.POST['item_index'])
        order = {}
        error = {}
        for k in range(1, k + 1):
            order['item_name_' + str(k)] = request.POST['item_name_' + str(k)]
            order['quantity_' + str(k)] = request.POST['quantity_' + str(k)]
            order['amount_' + str(k)] = request.POST['amount_' + str(k)]
            self.frozen_price = self.frozen_price + int(order['quantity_' + str(k)]) * int(order['amount_' + str(k)])
        restaurant = Restaurant.objects.get(pk=kwargs['restaurant_id'])
        group = Group.objects.get(pk=kwargs['group_id'])
        # The actual price for the food.
        price = self.frozen_price
        order['price'] = price
        # The price which need to be frozen.
        self.frozen_price = self.frozen_price + restaurant.restaurantserviceinfo.delivery_fee
        if self.request.user.customer.available_balance < self.frozen_price:
            error['top_up_information'] = "You don't have enough balance, please top up first"
            return render(request, self.template_name, error)
        else:
            new_personal_order = PersonalOrder.objects.create(price=price, order_time=timezone.now(),
                                                              customer_id=self.request.user.customer.id,
                                                              group_id=group.id)
            self.request.user.customer.available_balance = self.request.user.customer.available_balance \
                                                           - self.frozen_price
            self.request.user.customer.frozen_balance = self.request.user.customer.frozen_balance + self.frozen_price
            self.request.user.customer.save()
            self.personal_order_id = new_personal_order.id
            for k in range(1, k + 1):
                new_order_food = OrderFood.objects.create(count=order['quantity_' + str(k)],
                                                          food_id=Food.objects.filter(restaurant=restaurant.id).get(
                                                              name=order['item_name_' + str(k)]).id,
                                                          personal_order_id=self.personal_order_id)
            return self.get(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(CustomerRestaurantCheckOutView, self).get_queryset()
        queryset = queryset.filter(personal_order_id=self.personal_order_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CustomerRestaurantCheckOutView, self).get_context_data(**kwargs)
        context['delivery_fee'] = Restaurant.objects.get(
            pk=self.kwargs['restaurant_id']).restaurantserviceinfo.delivery_fee
        context['price'] = self.frozen_price
        return context


class CustomerWalletView(CustomerRequiredMixin, TemplateView):
    template_name = 'ET_Cust/Customer Account (Profile & Wallet).html'

    def get_context_data(self, **kwargs):
        context = super(CustomerWalletView, self).get_context_data(*kwargs)
        context['customer'] = self.request.user.customer
        return context


class CustomerOrderView(CustomerRequiredMixin, ListView):
    template_name = 'ET_Cust/Customer Account (Order).html'
    model = PersonalOrder
    context_object_name = "order_list"
    paginate_by = 3

    def get_queryset(self):
        queryset = super(CustomerOrderView, self).get_queryset()
        queryset = queryset.filter(customer_id=self.request.user.customer.id).order_by('-order_time')
        return queryset


def count_people(request, **kwargs):
    context = RequestContext(request)
    group_id = kwargs['group_id']
    count = 0
    if group_id:
        group = Group.objects.get(pk=group_id)
        if group:
            count = group.personalorder_set.count()
    return HttpResponse(count)

