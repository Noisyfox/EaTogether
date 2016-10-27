import uuid
from crispy_forms.layout import Submit
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as UserGroup
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.template import RequestContext
from django.views.generic import View, TemplateView, DetailView
from django.views.generic import FormView, CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from ET.forms import FormHelper
from ET.mixins import QueryMixin
from ET.models import Customer, Group, Restaurant, Food, OrderFood, PersonalOrder
from ET.views import LoginView, RegisterView
from ET_Cust.forms import CustomerLoginForm, CustomerRegisterForm, CustomerSearchRestaurantForm, \
    CustomerSearchAddressForm
from ET_Cust.mixins import CustomerRequiredMixin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ET_Cust.tasks import on_group_created
from bootstrap3_duration.widgets import DurationPicker


class AddressMixin(QueryMixin):
    _address = None
    _location = None

    def do_query(self, request, *args, **kwargs):
        if 'address' in request.session and 'location' in request.session:
            self._address = request.session['address']
            self._location = request.session['location']

    def get_context_data(self, **kwargs):
        context = super(AddressMixin, self).get_context_data(**kwargs)
        context['address'] = self._address
        context['location'] = self._location
        return context

    @property
    def address(self):
        return self._address

    @property
    def location(self):
        return self._location

    def set_address(self, address, location):
        self._address = address
        self._location = location

        self.request.session['address'] = address
        self.request.session['location'] = location


class AddressRequiredMixin(AddressMixin):
    def get(self, request, *args, **kwargs):
        if not self.address:
            return HttpResponseRedirect(reverse_lazy('cust_search'))

        return super(AddressRequiredMixin, self).get(request, *args, **kwargs)


class RestaurantQueryMixin(AddressMixin):
    _restaurant = None

    def do_query(self, request, *args, **kwargs):
        super(RestaurantQueryMixin, self).do_query(request, *args, **kwargs)

        self._restaurant = get_object_or_404(Restaurant, pk=kwargs['restaurant_id'])

    def get_context_data(self, **kwargs):
        context = super(RestaurantQueryMixin, self).get_context_data(**kwargs)
        context['restaurant'] = self._restaurant
        return context

    @property
    def restaurant(self):
        if not self._restaurant:
            raise Http404('Unknown restaurant.')

        return self._restaurant


class CustomerRegisterView(RegisterView):
    form_class = CustomerRegisterForm
    template_name = 'ET_Cust/customer_register.html'
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
    template_name = 'ET_Cust/customer_login.html'
    success_url = reverse_lazy('cust_search')

    def get_login_url(self):
        return reverse_lazy('cust_login')

    def get_signup_url(self):
        return reverse_lazy('cust_register')


class CustomerSearchView(AddressMixin, FormView):
    form_class = CustomerSearchAddressForm
    template_name = 'ET_Cust/customer_search.html'
    success_url = reverse_lazy('cust_main_page')

    def get(self, request, *args, **kwargs):
        if 'stay' not in request.GET and self.address and self.location:
            return HttpResponseRedirect(self.get_success_url())

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.set_address(form.cleaned_data['address'], form.cleaned_data['location'])

        return super(CustomerSearchView, self).form_valid(form)


class CustomerMainPageView(AddressRequiredMixin, ListView):
    template_name = 'ET_Cust/customer_main_page.html'
    model = Restaurant
    context_object_name = 'restaurant_list'

    def get_context_data(self, **kwargs):
        context = super(CustomerMainPageView, self).get_context_data(**kwargs)
        form = CustomerSearchRestaurantForm()
        context['form'] = form
        try:
            customer = self.request.user.customer
        except Exception:
            pass
        else:
            context['customer'] = customer
        return context

    def post(self, request, *args, **kwargs):
        form = CustomerSearchRestaurantForm(request.POST)
        if form.is_valid():
            self.queryset = self.queryset.filter(name__contains=form.cleaned_data['restaurant'])
            return self.get(self, request, *args, **kwargs)
        else:
            return self.get(self, request, *args, **kwargs)

    def get_queryset(self):
        location_search = GEOSGeometry(self.location, srid=4326)
        qs = Restaurant.objects.annotate(distance=Distance('location', location_search)).order_by('distance')
        qs = qs.annotate(favorite_restaurant=Distance('location', location_search))
        return qs


class CustomerRestaurantGroupView(CustomerRequiredMixin, RestaurantQueryMixin, ListView):
    template_name = 'ET_Cust/customer_restaurant_group_page.html'
    model = Group
    context_object_name = 'group_list'

    def get_queryset(self, **kwargs):
        queryset = super(CustomerRestaurantGroupView, self).get_queryset(**kwargs)
        queryset = queryset.filter(restaurant=self.restaurant).filter(status='G')
        return queryset


class CustomerCreateGroupView(CustomerRequiredMixin, RestaurantQueryMixin, CreateView):
    template_name = 'ET_Cust/customer_create_group.html'
    model = Group
    fields = ['destination', 'location', 'group_time']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['group_time'].widget = DurationPicker()
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Create'))
        return form

    def form_valid(self, form, **kwargs):
        group = form.save(commit=False)
        group.restaurant = self.restaurant
        group.save()

        on_group_created(group)

        return super(CustomerCreateGroupView, self).form_valid(form)

    def get_initial(self):
        init = super().get_initial()

        if self.location:
            init['destination'] = self.address
            init['location'] = self.location

        return init


class CustomerRestaurantMenuView(CustomerRequiredMixin, RestaurantQueryMixin, ListView):
    template_name = 'ET_Cust/customer_restaurant_menu_page.html'
    model = Food
    context_object_name = 'food_list'

    def get_context_data(self, **kwargs):
        context = super(CustomerRestaurantMenuView, self).get_context_data(**kwargs)
        context['food_list'] = context['food_list'].filter(restaurant=self.restaurant)
        context['group'] = self.kwargs['group_id']
        return context


class CustomerRestaurantCheckOutView(CustomerRequiredMixin, RestaurantQueryMixin, ListView):
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
        group = Group.objects.get(pk=kwargs['group_id'])
        # The actual price for the food.
        price = self.frozen_price
        order['price'] = price
        # The price which need to be frozen.
        self.frozen_price = self.frozen_price + self.restaurant.restaurantserviceinfo.delivery_fee
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
                                                          food_id=Food.objects.filter(restaurant=self.restaurant).get(
                                                              name=order['item_name_' + str(k)]).id,
                                                          personal_order_id=self.personal_order_id)
            return self.get(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(CustomerRestaurantCheckOutView, self).get_queryset()
        queryset = queryset.filter(personal_order_id=self.personal_order_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CustomerRestaurantCheckOutView, self).get_context_data(**kwargs)
        context['delivery_fee'] = self.restaurant.restaurantserviceinfo.delivery_fee
        context['price'] = self.frozen_price
        return context


class CustomerWalletView(CustomerRequiredMixin, AddressMixin, TemplateView):
    template_name = 'ET_Cust/Customer Account (Profile & Wallet).html'

    def get_context_data(self, **kwargs):
        context = super(CustomerWalletView, self).get_context_data(*kwargs)
        context['customer'] = self.request.user.customer
        return context


class CustomerOrderView(CustomerRequiredMixin, AddressMixin, ListView):
    template_name = 'ET_Cust/Customer Account (Order).html'
    model = PersonalOrder
    context_object_name = 'order_list'
    paginate_by = 3

    def get_queryset(self):
        queryset = super(CustomerOrderView, self).get_queryset()
        queryset = queryset.filter(customer_id=self.request.user.customer.id).order_by('-order_time')
        return queryset


class CustomerFavoriteView(CustomerRequiredMixin, AddressMixin, ListView):
    template_name = 'ET_Cust/Customer Account (Favourite).html'
    context_object_name = 'restaurant_list'

    def get_queryset(self):
        queryset = self.request.user.customer.favourite_restaurants.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CustomerFavoriteView, self).get_context_data(**kwargs)
        context['customer'] = self.request.user.customer
        return context


def count_people(request, **kwargs):
    context = RequestContext(request)
    group_id = kwargs['group_id']
    count = 0
    if group_id:
        group = Group.objects.get(pk=group_id)
        if group:
            count = group.personalorder_set.count()
    return HttpResponse(count)


class AddFavoriteView(View):
    def get(self, request, *args, **kwargs):
        restaurant_id = self.kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        try:
            customer = self.request.user.customer
        except Exception:
            return HttpResponse("Please log in first.")
        else:
            customer.favourite_restaurants.add(restaurant)
            return HttpResponse("Add to Favorite successfully!")


class DeleteFavoriteView(View):
    def get(self, request, *args, **kwargs):
        restaurant_id = self.kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        try:
            customer = self.request.user.customer
        except Exception:
            return HttpResponse("Please log in first.")
        else:
            customer.favourite_restaurants.remove(restaurant)
            return HttpResponse("Remove from Favorite successfully!")


def count_current_group(request, **kwargs):
    restaurant_id = kwargs['restaurant_id']
    count = 0
    if restaurant_id:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        if restaurant:
            count = restaurant.check_active_group()
    return HttpResponse(count)
