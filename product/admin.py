from django.contrib import admin
from product import models

# Register your models here.
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Category)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Product)