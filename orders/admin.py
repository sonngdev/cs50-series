from django.contrib import admin
from .models import RegularPizza, SicilianPizza, Topping, Sub, SubAddon, Pasta, Salad, DinnerPlatter

# Register your models here.
admin.site.register(RegularPizza)
admin.site.register(SicilianPizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(SubAddon)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerPlatter)
