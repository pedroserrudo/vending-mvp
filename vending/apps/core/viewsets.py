# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


def test(request):
    # test logout all
    u = User.objects.get(pk=1)
    u.get_session_auth_hash()