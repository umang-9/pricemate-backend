from django.contrib import admin
from .models import Product, Price, ProductRequest


admin.site.register(Product)
admin.site.register(Price)
admin.site.register(ProductRequest)
