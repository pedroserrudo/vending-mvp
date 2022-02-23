from abc import ABC

from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from vending.apps.vauth.models import VendingUser


class MultiTokenSerializer(serializers.Serializer):
    token = serializers.CharField(
        label=_("Token"),
        required=True
    )


class VendingUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=VendingUser.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, )
    role = serializers.ChoiceField(choices=VendingUser.ROLE_CHOICES)

    class Meta:
        model = VendingUser
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'role')

    def create(self, validated_data):
        user = VendingUser.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.role = validated_data['role']
        user.save()
        return user
