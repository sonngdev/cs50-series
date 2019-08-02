from django.db import models

# Create your models here.
class RegularPizza(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)
    topping_size = models.IntegerField(default=0)

class SicilianPizza(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)
    topping_size = models.IntegerField(default=0)

class Topping(models.Model):
    name = models.CharField(max_length=64)

class Sub(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)
    extra_cheese = models.BooleanField(default=False)

class SubAddon(models.Model):
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name='addons')
    name = models.CharField(max_length=64)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)

class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField(null=True, blank=True)

class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField(null=True, blank=True)

class DinnerPlatter(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)
