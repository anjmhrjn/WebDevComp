from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Experience(models.Model):
    experience_title = models.CharField(max_length=100)
    experience_description = models.TextField()
    shared_by = models.CharField(max_length=50, default="Anonymous")
    photo = models.ImageField(upload_to='media')


class Table(models.Model):
    table_name = models.CharField(max_length=20)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.table_name


class Reservations(models.Model):
    table_name = models.ForeignKey(Table, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_contact = models.CharField(max_length=10)
    registration_date = models.DateTimeField()
    no_of_seats = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "Reservation"

