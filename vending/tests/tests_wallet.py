import json

from django.test import TestCase

from rest_framework.test import APIClient, APIRequestFactory

from vending.apps.vauth.models import VendingUser


class TestWallet(TestCase):

    username_buyer = 'user_test_buyer'
    password_buyer = '123456abcdef_-^'
    token_buyer = None
    user_buyer = None

    username_seller = 'user_test_seller'
    password_seller = '123123123'
    token_seller = None
    user_seller = None

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def setup_buyer(self):
        self.client.post('/api/v1/users/', {'username': self.username_buyer,
                                            'password': self.password_buyer,
                                            'role': VendingUser.BUYER})

        resp_auth = self.client.post('/api/v1/auth/login', {'username': self.username_buyer,
                                                            'password': self.password_buyer})

        self.token_buyer = json.loads(resp_auth.content)['token']

    def setup_seller(self):
        self.client.post('/api/v1/users/', {'username': self.username_seller,
                                            'password': self.password_seller,
                                            'role': VendingUser.SELLER})

        resp_auth = self.client.post('/api/v1/auth/login', {'username': self.username_seller,
                                                            'password': self.password_seller})

        self.token_seller = json.loads(resp_auth.content)['token']

    def test_1_deposit(self):
        self.setup_buyer()
        self.setup_seller()

        auth_client = self.client
        auth_client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_buyer}')
        balance_resp = auth_client.get('/api/v1/wallet/balance')
        self.assertEqual(0, json.loads(balance_resp.content)['balance'])

        deposit_resp = auth_client.post('/api/v1/wallet/deposit', {'coins': [10, 20, 20, 50, 100]})  # 200 coins
        self.assertEqual(200, json.loads(deposit_resp.content)['balance'])

        balance_resp = auth_client.get('/api/v1/wallet/balance')
        self.assertEqual(200, json.loads(balance_resp.content)['balance'])

        reset_resp = auth_client.get('/api/v1/wallet/reset')
        self.assertEqual(0, json.loads(reset_resp.content)['balance'])



