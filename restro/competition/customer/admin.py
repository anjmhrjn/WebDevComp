from django.contrib import admin
from .models import ItemType, Menu, Order, OrderCount

# Register your models here.
admin.site.register(ItemType)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderCount)
# admin.site.register(Experience)
