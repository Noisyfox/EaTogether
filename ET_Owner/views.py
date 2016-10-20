import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from ET.models import Owner, Food, Restaurant, Courier, RestaurantServiceInfo
from ET.views import RegisterView, LoginView
from ET_Owner.forms import OwnerRegisterForm, OwnerLoginForm, FoodEditForm, RestaurantEditForm
from ET_Owner.mixins import RestaurantRequiredMixin, OwnerRequiredMixin


class OwnerRegisterView(RegisterView):
    form_class = OwnerRegisterForm
    template_name = 'ET_Owner/owner_register.html'
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
    template_name = 'ET_Owner/owner_login.html'
    success_url = reverse_lazy('owner_order_list')

    def get_login_url(self):
        return reverse_lazy('owner_login')

    def get_signup_url(self):
        return reverse_lazy('owner_register')


class OwnerOrderListView(RestaurantRequiredMixin, TemplateView):
    template_name = 'ET_Cust/homepage.html'


class OwnerRestaurantEditView(OwnerRequiredMixin, UpdateView):
    model = Restaurant
    form_class = RestaurantEditForm
    template_name = 'ET_Owner/owner_my_restaurant.html'
    success_url = reverse_lazy('owner_edit_restaurant')

    def get_object(self, queryset=None):
        try:
            return self.request.user.owner.restaurant
        except ObjectDoesNotExist:
            return None

    def form_valid(self, form):
        if not self.object:
            restaurant = form.save(commit=False)
            restaurant.owner = self.request.user.owner

            restaurant.save()

            RestaurantServiceInfo(restaurant=restaurant).save()

            self.object = restaurant

        return super(OwnerRestaurantEditView, self).form_valid(form)


class OwnerMenuView(RestaurantRequiredMixin, ListView):
    template_name = 'ET_Owner/owner_menu.html'
    allow_empty = True
    context_object_name = 'foods'

    def get_queryset(self):
        return Food.objects.filter(restaurant=self.request.user.owner.restaurant)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['restaurant'] = self.request.user.owner.restaurant
        ctx['service'], _ = RestaurantServiceInfo.objects.get_or_create(
            restaurant=self.request.user.owner.restaurant)

        return ctx


class OwnerFoodCreateView(RestaurantRequiredMixin, CreateView):
    model = Food
    form_class = FoodEditForm
    template_name = 'ET_Owner/owner_edit_food.html'
    success_url = reverse_lazy('owner_menu')
    context_object_name = 'food'

    def form_valid(self, form):
        food = form.save(commit=False)
        food.restaurant = self.request.user.owner.restaurant
        return super(OwnerFoodCreateView, self).form_valid(form)


class OwnerFoodEditView(RestaurantRequiredMixin, UpdateView):
    model = Food
    form_class = FoodEditForm
    template_name = 'ET_Owner/owner_edit_food.html'
    success_url = reverse_lazy('owner_menu')
    context_object_name = 'food'


class OwnerCourierView(RestaurantRequiredMixin, ListView):
    template_name = 'ET_Owner/owner_delivery.html'
    allow_empty = True
    context_object_name = 'couriers'

    def get_queryset(self):
        return Courier.objects.filter(restaurant=self.request.user.owner.restaurant)


class OwnerCourierCreateView(RestaurantRequiredMixin, CreateView):
    model = Food
    form_class = FoodEditForm
    template_name = 'ET_Owner/owner_edit_food.html'
    success_url = reverse_lazy('owner_menu')
    context_object_name = 'food'

    def form_valid(self, form):
        food = form.save(commit=False)
        food.restaurant = self.request.user.owner.restaurant
        return super(OwnerCourierCreateView, self).form_valid(form)
