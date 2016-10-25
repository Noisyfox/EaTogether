import uuid

from django.db import transaction

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from ET.mixins import QueryMixin
from ET.models import Owner, Food, Restaurant, Courier, RestaurantServiceInfo, GroupOrder
from ET.views import RegisterView, LoginView
from ET_Cour.templatetags.courier_name_tag import courier_name
from ET_Owner.forms import OwnerRegisterForm, OwnerLoginForm, FoodEditForm, RestaurantEditForm, CourierEditForm, \
    FoodDeliveryForm
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
            user.groups.add(Group.objects.get(name__exact=group))
        except Exception:
            user.delete()
            raise

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


class OwnerCourierCreateView(RestaurantRequiredMixin, FormView):
    form_class = CourierEditForm
    template_name = 'ET_Owner/owner_edit_courier.html'
    success_url = reverse_lazy('owner_courier')

    def form_valid(self, form):
        User = get_user_model()

        username = 'cid_%s_%s' % (self.request.user.owner.phone_number, form.cleaned_data['login_id'])
        if User.objects.filter(username=username).exists():
            form.add_error('login_id', _('This login id is already taken. Please input another.'))
            return self.form_invalid(form)

        user = User()
        user.username = username
        user.first_name = form.cleaned_data['name']
        user.set_password(form.cleaned_data['password'])

        user.save()

        try:
            c = Courier(restaurant=self.request.user.owner.restaurant, user=user)
            c.save()
        except Exception:
            user.delete()
            raise

        user.groups.add(Group.objects.get(name__exact='courier'))
        user.save()

        return super(OwnerCourierCreateView, self).form_valid(form)


class CourierQueryMixin(QueryMixin):
    def do_query(self, request, *args, **kwargs):
        self._courier = get_object_or_404(Courier, pk=kwargs['pk'])

    @property
    def courier(self):
        if not self._courier:
            raise Http404('Unknown courier.')

        return self._courier

    def get_context_data(self, **kwargs):
        ctx = super(CourierQueryMixin, self).get_context_data(**kwargs)

        ctx['courier'] = self._courier

        return ctx


class OwnerCourierEditView(RestaurantRequiredMixin, CourierQueryMixin, FormView):
    form_class = CourierEditForm
    template_name = 'ET_Owner/owner_edit_courier.html'
    success_url = reverse_lazy('owner_courier')

    def get_initial(self):
        init = super().get_initial()

        init.update({
            'name': self.courier.user.first_name,
            'login_id': courier_name(self.courier.user.username)
        })

        return init

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['login_id'].disabled = True
        form.fields['password'].required = False

        return form

    def form_valid(self, form):
        user = self.courier.user

        if 'password' in form.cleaned_data and form.cleaned_data['password']:
            user.set_password(form.cleaned_data['password'])

        user.first_name = form.cleaned_data['name']

        user.save()

        return super(OwnerCourierEditView, self).form_valid(form)


class AssignmentDeleteView(RestaurantRequiredMixin, CourierQueryMixin, DeleteView):
    template_name = 'ET_Owner/owner_delete_courier.html'

    def get_object(self, queryset=None):
        return self.courier.user

    def get_success_url(self):
        return reverse_lazy('owner_courier')


class WalletView(RestaurantRequiredMixin, TemplateView):
    template_name = 'ET_Owner/owner_wallet.html'


class OrderListView(RestaurantRequiredMixin, ListView):
    template_name = 'ET_Owner/owner_orders.html'
    context_object_name = 'orders'
    allow_empty = True

    def get_queryset(self):
        return GroupOrder.objects.filter(group__restaurant=self.request.user.owner.restaurant).order_by('-submit_time')


class OrderQueryMixin(QueryMixin):
    def do_query(self, request, *args, **kwargs):
        self._order = get_object_or_404(GroupOrder, pk=kwargs['order_id'])

        if self._order.group.restaurant != self.request.user.owner.restaurant:
            raise PermissionError

    @property
    def order(self):
        if not self._order:
            raise Http404('Unknown order.')

        return self._order

    def get_context_data(self, **kwargs):
        ctx = super(OrderQueryMixin, self).get_context_data(**kwargs)

        ctx['order'] = self._order

        return ctx


class OrderAcceptView(RestaurantRequiredMixin, OrderQueryMixin, View):
    def get(self, request, *args, **kwargs):
        if not self.order.accepted:
            self.order.status = 'A'
            self.order.accept_time = timezone.now()
            self.order.save()

        return HttpResponseRedirect(reverse_lazy('owner_order_list'))


class OrderDeliveryView(RestaurantRequiredMixin, OrderQueryMixin, FormView):
    form_class = FoodDeliveryForm
    template_name = 'ET_Owner/owner_order_delivery.html'
    success_url = reverse_lazy('owner_order_list')

    def get_form_kwargs(self):
        init = super().get_form_kwargs()

        init.update({
            'couriers': Courier.objects.filter(restaurant=self.request.user.owner.restaurant),
        })

        return init

    def form_valid(self, form):
        with transaction.atomic():
            if self.order.delivery_started:
                form.add_error(field=None, error=_('This order has already been delivered!'))
                return self.form_invalid(form)
            courier = form.cleaned_data['courier']

            self.order.status = 'D'
            self.order.delivery_start_time = timezone.now()
            self.order.courier = courier
            for order_p in self.order.personal_orders:
                order_p.status = 'D'
                order_p.save()
            self.order.save()

        return super().form_valid(form)
