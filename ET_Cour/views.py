from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView

from ET.mixins import QueryMixin
from ET.models import GroupOrder, PersonalOrder
from ET.views import LoginView
from ET_Cour.forms import CourierLoginForm
from ET_Cour.mixins import CourierRequiredMixin


class CourierLoginView(LoginView):
    form_class = CourierLoginForm
    template_name = 'ET_Cour/login.html'
    success_url = reverse_lazy('cour_order')

    def get_login_url(self):
        return reverse_lazy('cour_login')


class CourierOrderListView(CourierRequiredMixin, ListView):
    template_name = 'ET_Cour/order.html'
    context_object_name = 'orders'
    allow_empty = True

    def get_queryset(self):
        return self.request.user.courier.grouporder_set.order_by('-delivery_start_time')


class OrderQueryMixin(QueryMixin):
    def do_query(self, request, *args, **kwargs):
        self._order = get_object_or_404(GroupOrder, pk=kwargs['order_id'])

        if self._order.courier != request.user.courier:
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


class PersonalOrderQueryMixin(OrderQueryMixin):
    def do_query(self, request, *args, **kwargs):
        super(PersonalOrderQueryMixin, self).do_query(request, *args, **kwargs)

        self._personal_order = get_object_or_404(PersonalOrder, pk=kwargs['personal_order_id'])

        if self._order.group != self._personal_order.group:
            raise Http404('Unknown personal order.')

    @property
    def personal_order(self):
        if not self._personal_order:
            raise Http404('Unknown personal order.')

        return self._personal_order

    def get_context_data(self, **kwargs):
        ctx = super(PersonalOrderQueryMixin, self).get_context_data(**kwargs)

        ctx['personal_order'] = self._personal_order

        return ctx


class CourierOrderDetailView(CourierRequiredMixin, OrderQueryMixin, DetailView):
    template_name = 'ET_Cour/detail.html'

    def get_object(self, queryset=None):
        return self.order


class CourierPersonalOrderFinishView(CourierRequiredMixin, PersonalOrderQueryMixin, View):
    status = None

    ALLOWED_STATUS = ['U', 'F']

    def __init__(self, **kwargs):
        self.status = kwargs.pop('status')
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        if self.status not in self.ALLOWED_STATUS:
            raise ImproperlyConfigured("Status not allowed!")

        with transaction.atomic():
            if not self.personal_order.finished:
                self.personal_order.status = self.status
                self.personal_order.save()

                if not self.order.personal_orders.exclude(status__in=self.ALLOWED_STATUS).exists():
                    self.order.status = 'F'
                    self.order.confirm_delivery_time = timezone.now()
                    self.order.save()

                    # Send money to owner
                    owner = self.order.group.restaurant.owner
                    owner.money = F('money') + self.order.price_total
                    owner.save()

        return HttpResponseRedirect(reverse_lazy('cour_detail', kwargs={'order_id': self.order.pk}))
