from django.urls import re_path

from vending.apps.vauth.api_views import ObtainAuthToken, KillAuthToken, KillAllAuthTokens


urlpatterns = [
    re_path('login/?$', ObtainAuthToken.as_view()),
    re_path('logout/?$', KillAuthToken.as_view()),
    re_path('logout-all/?$', KillAllAuthTokens.as_view()),
]
