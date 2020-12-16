from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
# categories prepared to create dropdown option in admin page
categories = [
    ('food', 'FOOD'),
    ('dessert', 'DESSERT'),
    ('drink', 'DRINK')
]


class ItemType(models.Model):
    item_type = models.CharField(max_length=50)
    item_category = models.CharField(max_length=20, choices=categories, default='food')

    class Meta:
        verbose_name = 'Type'

    def __str__(self):
        return self.item_type


# class Menu for creating a database model
class Menu(models.Model):
    # attributes of Menu model
    item_name = models.CharField(max_length=200)
    description = models.TextField()
    stock = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.FloatField(validators=[MinValueValidator(1)])
    item_type = models.ForeignKey(ItemType, on_delete=models.SET_NULL, blank=True, null=True)
    # item_type = models.CharField(max_length=8, choices=categories, default='food')
    ordered_by = models.ManyToManyField(User, through='Order')

    def __str__(self):
        return self.item_name


# # status prepared to create dropdown option in admin page
status = [
    ('delivered', 'DELIVERED'),
    ('cancelled', 'CANCELED'),
    ('in process', 'IN PROCESS'),
    ('processed', 'PROCESSED')
]


# class Order for creating a database model
class Order(models.Model):
    # attributes of Order model
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    item = models.ForeignKey(Menu, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(default=timezone.now)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    order_status = models.CharField(max_length=12, choices=status, default='in process')

    def __str__(self):
        return self.order_status


# # class Experience for creating a database model
# class Experience(models.Model):
#     # attributes of Experience model
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service = models.IntegerField(validators=[MinValueValidator(1)])
#     food = models.IntegerField(validators=[MinValueValidator(1)])
#     date_registered = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.service
