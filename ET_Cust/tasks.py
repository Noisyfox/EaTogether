from __future__ import absolute_import

from celery import shared_task
from django.db import transaction
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
            GroupOrder(group=group).save()
            # TODO: notify restaurant


def on_group_created(group):
    submit_group_order.apply_async(kwargs={'pk': group.pk}, eta=group.exceed_time)
