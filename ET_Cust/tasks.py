from __future__ import absolute_import

from celery import shared_task
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from ET.models import Group, GroupOrder


@shared_task(bind=True)
def submit_group_order(self, pk):
    group = Group.objects.get(pk=pk)

    print("Task run on %s, except on %s\n" % (timezone.now(), group.exceed_time))

    with transaction.atomic():
        if group.status == 'O':
            raise RuntimeError('Already submitted!')

        group.status = 'O'
        group.save()

        # Do not create an order for an empty group
        if group.personalorder_set.exists():
            order = GroupOrder(group=group)
            order.frozen_price()
            order.save()

            for p in order.personal_orders:
                # Submit personal order
                p.status = 'S'

                # Calculate every one's delivery fee
                p.update_delivery_fee(order.price_food, order.price_delivery)
                p.save()

                cust = p.customer
                # Update user's wallet
                cust.frozen_balance -= (p.price + p.delivery_fee)

                # Check user's order
                if not cust.personalorder_set.filter(status='W').exists():
                    # All orders are submitted, so we can return all remain frozen balance
                    cust.available_balance += cust.frozen_balance
                    cust.frozen_balance = 0

                cust.save()
                # TODO: notify restaurant


def on_group_created(group):
    submit_group_order.apply_async(kwargs={'pk': group.pk}, eta=group.exceed_time)
