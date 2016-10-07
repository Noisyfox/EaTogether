from django.db import models
from django.conf import settings

class Courier(models.Model):
    courier_login_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)

class Restaurant(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    introduction = models.TextField()
    state = models.SlugField(max_length=3)  # The max length of the state abbr in Australia is 3.
    address = models.TextField()
    logo = models.URLField()
    money = models.FloatField()
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
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
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
    group_id = models.OneToOneField(Group, on_delete=models.CASCADE)
    courier_id = models.ForeignKey(Courier, on_delete=models.CASCADE)

class Customer(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    balance = models.FloatField()

# Suggest change to the many to many relation directly.
class FavoriteRestaurant(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class PersonalOrder(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    group_id = models.ForeignKey(GroupOrder, on_delete=models.CASCADE)
    price = models.FloatField()
    delivery_fee = models.FloatField()
    ordertime = models.DateTimeField()

class OrderFood(models.Model):
    personal_order = models.ForeignKey(PersonalOrder, on_delete=models.CASCADE)
    food_id = models.ManyToManyField(Food)
    count = models.SmallIntegerField()

