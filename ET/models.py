from django.db import models
from django.conf import settings


class Courier(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)


class Owner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, unique=True)
    money = models.FloatField(default=0)


class Restaurant(models.Model):
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)

    # Restaurant information
    name = models.CharField(max_length=30)

    # Contact info
    contact_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)

    introduction = models.TextField()
    state = models.SlugField(max_length=3)  # The max length of the state abbr in Australia is 3.
    address = models.TextField()
    logo = models.URLField()
    # Validation infomation.
    id_photo = models.URLField()
    business_license = models.URLField()


class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    introduction = models.TextField()
    picture = models.URLField()
    price = models.FloatField()


class Group(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    group_time = models.TimeField()
    create_time = models.DateTimeField()

    # Exceed_time can be calculated based on group_time and create_time.
    # exceed_time = models.DateTimeField()
    # Joined_time can be omitted actually.

    accept_time = models.DateTimeField()
    delivery_start_time = models.DateTimeField()
    confirm_delivery_time = models.DateTimeField()
    destination = models.TextField()

    # Order_id actually is not needed in this case.


class GroupOrder(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, unique=True)
    balance = models.FloatField(default=0)
    favourite_restaurants = models.ManyToManyField(Restaurant, blank=True)


class PersonalOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupOrder, on_delete=models.CASCADE)
    price = models.FloatField()
    delivery_fee = models.FloatField()
    order_time = models.DateTimeField()


class OrderFood(models.Model):
    personal_order = models.ForeignKey(PersonalOrder, on_delete=models.CASCADE)
    food = models.ManyToManyField(Food)
    count = models.SmallIntegerField()
