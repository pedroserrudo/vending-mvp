import binascii
import os

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property


class VendingUser(AbstractUser):
    BUYER, SELLER = "buyer", "seller"
    ROLE_CHOICES = (
        (BUYER, "Buyer"),
        (SELLER, "Seller")
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=10, default=BUYER)
    deposit = models.PositiveIntegerField(default=0)

    @cached_property
    def is_buyer(self):
        return bool(self.role == self.BUYER)

    @cached_property
    def is_seller(self):
        return bool(self.role == self.SELLER)


class MultiToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ForeignKey(
        VendingUser, related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("MultiToken")
        verbose_name_plural = _("MultiTokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key