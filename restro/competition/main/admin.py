from django.contrib import admin
from .models import Menu, Order, Experience


# Register your models here.

# this class is prepared to group different fields and create a field set
class MenuAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name/Price', {"fields": ["item_name", "price"]}),
        ('Description', {"fields": ["description"]}),
        ('Stock', {"fields": ["stock"]}),
        ('Type', {"fields": ["item_type"]})
    ]


admin.site.register(Menu, MenuAdmin)
admin.site.register(Order)
admin.site.register(Experience)
