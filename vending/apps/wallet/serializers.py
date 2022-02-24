from rest_framework import serializers
from rest_framework.fields import MultipleChoiceField, empty, html


class DuplicateMultipleChoiceField(MultipleChoiceField):

    def to_internal_value(self, data):
        if isinstance(data, str) or not hasattr(data, '__iter__'):
            self.fail('not_a_list', input_type=type(data).__name__)
        if not self.allow_empty and len(data) == 0:
            self.fail('empty')

        return [
            super(MultipleChoiceField, self).to_internal_value(item)
            for item in data
        ]


class DepositWalletSerializer(serializers.Serializer):
    COIN_CHOICES = (
        (100, '100 cents'),
        (50, '50 cents'),
        (20, '20 cents'),
        (10, '10 cents'),
        (5, '5 cents')
    )  # choices must be ordered
    coins = DuplicateMultipleChoiceField(required=True, choices=COIN_CHOICES, allow_empty=False)

