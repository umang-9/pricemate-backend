from django.contrib import admin
from .models import Product, Price, ProductRequest, Watch


admin.site.register(Product)
admin.site.register(Price)
admin.site.register(ProductRequest)
admin.site.register(Watch)
