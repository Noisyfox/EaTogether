import re

from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.urls import reverse
from location_field.models.spatial import LocationField


class Owner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, unique=True)
    money = models.FloatField(default=0)

    def __str__(self):
        return self.phone_number


class Restaurant(models.Model):
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)

    # Restaurant information
    name = models.CharField(max_length=30)

    # Contact info
    contact_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)

    introduction = models.TextField()
    address = models.CharField(max_length=255)
    location = LocationField(address_field='address', zoom=13)
    logo = models.ImageField()

    # Validation info
    id_number = models.CharField(max_length=50)
    id_photo = models.ImageField()
    business_license = models.ImageField()

    def check_active_group(self):
        count = self.group_set.filter(status='G').count()
        return count


class Courier(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

    @property
    def account(self):
        m = re.match(r"^cid_(?P<owner>.+?)_(?P<courier>.+)$", self.user.username)
        return m.group('courier')


class RestaurantServiceInfo(models.Model):
    SERV_STATUS = (
        ('O', 'Open'),
        ('C', 'Close'),
    )
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)

    min_delivery = models.FloatField(default=0, validators=[MinValueValidator(0)])
    delivery_fee = models.FloatField(default=0, validators=[MinValueValidator(0)])

    announcement = models.TextField(max_length=500, blank=True)

    service_status = models.CharField(max_length=1, choices=SERV_STATUS, default='C')


class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    introduction = models.TextField()
    picture = models.ImageField()
    price = models.FloatField()


class Group(models.Model):
    STATUS = (
        ('G', 'Grouping'),
        ('O', 'Over'),
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    group_time = models.DurationField()
    create_time = models.DateTimeField(auto_now_add=True)

    # Exceed_time can be calculated based on group_time and create_time.
    # exceed_time = models.DateTimeField()
    # Joined_time can be omitted actually.
    destination = models.CharField(max_length=255)
    location = LocationField(address_field='destination', zoom=13)
    status = models.CharField(max_length=1, choices=STATUS, default='G')

    # Order_id actually is not needed in this case.

    def get_absolute_url(self):
        return reverse('cust_restaurant_menu', kwargs={'restaurant_id': self.restaurant.id, 'group_id': self.pk})

    @property
    def exceed_time(self):
        return self.create_time + self.group_time


class GroupOrder(models.Model):
    STATUS = (
        ('W', 'Waiting'),
        ('A', 'Accepted'),
        ('D', 'Delivering'),
        ('F', 'Finished'),
    )

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=1, choices=STATUS, default='W')

    submit_time = models.DateTimeField(auto_now_add=True)
    accept_time = models.DateTimeField(null=True, blank=True)
    delivery_start_time = models.DateTimeField(null=True, blank=True)
    confirm_delivery_time = models.DateTimeField(null=True, blank=True)

    price_food = models.FloatField(default=0)
    price_delivery = models.FloatField(default=0)
    price_total = models.FloatField(default=0)

    @property
    def accepted(self):
        return self.status != 'W'

    @property
    def delivery_started(self):
        return self.status == 'D' or self.status == 'F'

    @property
    def finished(self):
        return self.status == 'F'

    @property
    def personal_orders(self):
        return self.group.personalorder_set.all()

    # Calculate price
    def frozen_price(self):
        price = 0
        for p in self.personal_orders:
            price += p.price

        self.price_food = price
        self.price_delivery = self.group.restaurant.restaurantserviceinfo.delivery_fee
        self.price_total = self.price_food + self.price_delivery


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, unique=True)
    available_balance = models.FloatField(default=0)
    frozen_balance = models.FloatField(default=0)
    favourite_restaurants = models.ManyToManyField(Restaurant, blank=True)

    def __str__(self):
        return self.phone_number


class PersonalOrder(models.Model):
    STATUS = (
        ('W', 'Waiting'),
        ('S', 'Submitted'),
        ('D', 'Delivering'),
        ('F', 'Delivered'),
        ('U', 'Undelivered'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    price = models.FloatField()
    delivery_fee = models.FloatField(null=True, blank=True)
    order_time = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=1, choices=STATUS, default='W')

    @property
    def foods(self):
        return self.orderfood_set.all()

    @property
    def finished(self):
        return self.delivered or self.undelivered

    @property
    def delivered(self):
        return self.status == 'F'

    @property
    def undelivered(self):
        return self.status == 'U'

    def update_delivery_fee(self, total_food_price, total_delivery_fee):
        if total_delivery_fee > 0:
            self.delivery_fee = round(total_delivery_fee * self.price / total_food_price, 2)
        else:
            self.delivery_fee = 0


class OrderFood(models.Model):
    personal_order = models.ForeignKey(PersonalOrder, on_delete=models.CASCADE)
    food = models.ForeignKey(Food)
    count = models.SmallIntegerField()

    @property
    def price(self):
        return self.food.price * self.count

