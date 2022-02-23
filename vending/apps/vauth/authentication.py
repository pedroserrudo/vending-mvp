
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication

from vending.apps.vauth.models import MultiToken


class MultipleTokenAuthentication(BaseTokenAuthentication):
    keyword = 'Token'
    model = MultiToken

