import json

from django.test import TestCase

from django.test import Client

from rest_framework import status
from rest_framework.test import RequestsClient, APIClient, APIRequestFactory

from vending.apps.vauth.models import VendingUser, MultiToken


class TestAuth(TestCase):

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

    def create_buyer(self):
        return self.client.post('/api/v1/users/', {'username': self.username_buyer,
                                                   'password': self.password_buyer,
                                                   'role': VendingUser.BUYER
                                                   })

    def create_seller(self):
        return self.client.post('/api/v1/users/', {'username': self.username_seller,
                                                   'password': self.password_seller,
                                                   'role': VendingUser.SELLER})

    def test_1_login_buyer(self):
        self.create_buyer()

        request = self.client.post('/api/v1/auth/login', {'username': self.username_buyer,
                                                          'password': self.password_buyer})
        json_resp = json.loads(request.content)
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertIn('token', json_resp)

        self.token_buyer = json_resp['token']

        bad_request = self.client.post('/api/v1/auth/login', {'username': self.username_buyer, 'password': 'asdasd'})
        self.assertEqual(bad_request.status_code, 400)

    def test_1_login_seller(self):
        self.create_seller()

        request = self.client.post('/api/v1/auth/login', {'username': self.username_seller, 'password': self.password_seller})

        json_resp = json.loads(request.content)
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertIn('token', json_resp)

        self.token_buyer = json_resp['token']

        bad_request = self.client.post('/api/v1/auth/login', {'username': self.username_seller, 'password': 'asdasd'})
        self.assertEqual(bad_request.status_code, 400)
