from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
    price = models.FloatField(null=True, blank=True)

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

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'Shopping cart of {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    price = models.FloatField(default=0)
    product_object_id = models.IntegerField()
    product_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)

    product = GenericForeignKey('product_content_type', 'product_object_id')

    def __str__(self):
        return f'{self.product_content_type} - {self.product.name} (${self.price})'
