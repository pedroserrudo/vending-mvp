# -*- coding: utf-8 -*-
from django.apps import AppConfig


class AffiliatesConfig(AppConfig):
    name = 'vending.apps.vauth'

    def ready(self):
        # from .receiver import *
        pass