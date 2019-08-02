from django.db import models

# Create your models here.
class RegularPizza(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)
    topping_size = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class SicilianPizza(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)
    item_size = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Sub(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class SubAddon(models.Model):
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name='addons')
    name = models.CharField(max_length=64)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class DinnerPlatter(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
