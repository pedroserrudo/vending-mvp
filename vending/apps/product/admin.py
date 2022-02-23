from django.contrib import admin

from vending.apps.product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cost', 'quantity', 'seller')
    list_filter = ('seller', )


admin.site.register(Product, ProductAdmin)
