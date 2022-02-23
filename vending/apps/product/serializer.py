from django.db import models
from rest_framework import serializers

from vending.apps.product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)

    class Meta:
        fields = ('id', 'name', 'cost', 'quantity', 'seller')
        model = Product


class BuyProductSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        try:
            product = Product.objects.get(pk=data['product'])
        except models.ObjectDoesNotExist as e:
            raise serializers.ValidationError('Product does not exist.') from e

        if product.quantity < data['quantity']:
            raise serializers.ValidationError('Invalid amount, {} available'.format(product.quantity))

        return data
