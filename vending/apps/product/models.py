from django.db import models
from django.utils.translation import gettext_lazy as _

from vending.apps.vauth.models import VendingUser


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Product Name'))
    cost = models.PositiveIntegerField(verbose_name=_('Product Cost'))
    quantity = models.PositiveIntegerField(verbose_name=_('Stock Available'))
    seller = models.ForeignKey(VendingUser, on_delete=models.SET_NULL, null=True, related_name='products')
    created_at = models.DateTimeField(_("Created"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated"), auto_now_add=False, auto_now=True, editable=False)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

