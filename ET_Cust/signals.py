from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from ET.models import Customer


def top_up_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        customer = Customer.objects.get(pk=ipn_obj.custom)
        customer.available_balance = customer.available_balance + float(ipn_obj.mc_gross)
        customer.save()

valid_ipn_received.connect(top_up_notification)
