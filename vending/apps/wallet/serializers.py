from rest_framework import serializers


class DepositWalletSerializer(serializers.Serializer):
    COIN_CHOICES = (
        (5, '5 cents'),
        (10, '10 cents'),
        (20, '20 cents'),
        (50, '50 cents'),
        (100, '100 cents')
    )
    coins = serializers.MultipleChoiceField(required=True, choices=COIN_CHOICES, allow_empty=False)
