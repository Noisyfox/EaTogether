from django.contrib import admin

# Register your models here.
from ET.models import Owner, Restaurant, Courier, RestaurantServiceInfo, Food, Group, GroupOrder, Customer, \
    PersonalOrder, OrderFood

admin.site.register(Owner)
admin.site.register(Restaurant)
admin.site.register(Courier)
admin.site.register(RestaurantServiceInfo)
admin.site.register(Food)
admin.site.register(Group)
admin.site.register(GroupOrder)
admin.site.register(Customer)
admin.site.register(PersonalOrder)
admin.site.register(OrderFood)
