from django.urls import path

from vending.apps.vauth.api_views import ObtainAuthToken, KillAuthToken, KillAllAuthTokens


urlpatterns = [
    path('login', ObtainAuthToken.as_view()),
    path('logout', KillAuthToken.as_view()),
    path('logout-all', KillAllAuthTokens.as_view()),
]