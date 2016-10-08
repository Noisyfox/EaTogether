from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from ET.models import Customer, Courier, Owner


class UniversalAuthenticationBackend(ModelBackend):
    def authenticate(self, username=None, password=None, group=None, **credentials):
        if group == 'customer':
            user = self.auth_customer(username)
        elif group == 'owner':
            user = self.auth_owner(username)
        elif group == 'courier':
            try:
                user = self.auth_courier(username, credentials['courier_id'])
            except KeyError:
                return None
        elif group == 'admin':
            user = self.auth_admin(username)
        else:
            return None

        if user is not None and user.check_password(password):
            return user

    @staticmethod
    def auth_customer(phone_number):
        try:
            customer = Customer.objects.get(phone_number__iexact=phone_number)
        except Customer.DoesNotExist:
            return None
        else:
            return customer.user

    @staticmethod
    def auth_owner(phone_number):
        try:
            owner = Owner.objects.get(phone_number__iexact=phone_number)
        except Owner.DoesNotExist:
            return None
        else:
            return owner.user

    @staticmethod
    def auth_courier(owner_phone_number, courier_id):
        courier_user_id = 'cid_%s_%s' % owner_phone_number, courier_id
        try:
            courier = Courier.objects.get(
                Q(restaurant__phone_number__iexact=owner_phone_number) & Q(user__username__iexact=courier_user_id))
        except Courier.DoesNotExist:
            return None
        else:
            return courier.user

    @staticmethod
    def auth_admin(user_name):
        admin_user_id = 'admin_%s' % user_name

        user_model = get_user_model()
        try:
            user = user_model.objects.get(username__iexact=admin_user_id)
        except user_model.DoesNotExist:
            return None
        else:
            return user
