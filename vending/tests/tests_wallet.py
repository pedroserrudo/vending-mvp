import json

from django.test import TestCase

from rest_framework import status
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
        """Create Buyer, Deposit Coins, Check Balance, Reset Balance"""
        self.setup_buyer()

        auth_client = self.client
        auth_client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_buyer}')
        balance_resp = auth_client.get('/api/v1/wallet/balance')
        self.assertEqual(0, json.loads(balance_resp.content)['balance'])

        # Deposit 200
        deposit_resp = auth_client.post('/api/v1/wallet/deposit', {'coins': [10, 20, 20, 50, 100]})  # 200 coins
        self.assertEqual(json.loads(deposit_resp.content)['balance'], 200)

        # Check Balance
        balance_resp = auth_client.get('/api/v1/wallet/balance')
        self.assertEqual(json.loads(balance_resp.content)['balance'], 200)

        # Reset Wallet
        reset_resp = auth_client.get('/api/v1/wallet/reset')
        self.assertEqual(json.loads(reset_resp.content)['balance'], 0)

    def test_2_buy(self):
        """Create Buyer and Seller, create Product, Update Product and Buy Product and Delete Product"""
        self.setup_buyer()
        self.setup_seller()

        # Create Product
        auth_client = self.client
        auth_client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_seller}')

        product_resp = auth_client.post('/api/v1/product/', {'name': 'coke', 'cost': 1, 'quantity': 10})
        self.assertEqual(product_resp.status_code, status.HTTP_201_CREATED)
        product_id = json.loads(product_resp.content)['id']

        # Update product Quantity
        update_product_resp = auth_client.patch(f'/api/v1/product/{product_id}/', {'quantity': 25})

        self.assertEqual(update_product_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(update_product_resp.content)['quantity'], 25)

        # Buyer Deposit
        auth_client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_buyer}')
        deposit_resp = auth_client.post('/api/v1/wallet/deposit', {'coins': [10, 20, 20, 50, 100]})  # 200 coins
        self.assertEqual(json.loads(deposit_resp.content)['balance'], 200)

        # Buy Product Fail
        buy_resp = auth_client.post('/api/v1/product/buy', {'product': product_id, 'quantity': 30})
        self.assertEqual(buy_resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Buy product OK
        buy_resp = auth_client.post('/api/v1/product/buy', {'product': product_id, 'quantity': 15})
        buy_json = json.loads(buy_resp.content)

        self.assertEqual(buy_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(buy_json['quantity'], 15)
        self.assertEqual(buy_json['total_spent'], 15)
        self.assertEqual(buy_json['change'], [100, 50, 20, 10, 5])
        self.assertEqual(buy_json['no-change'], 0)

        # Delete Product # check exists-> delete -> gone
        gone_product = auth_client.get(f'/api/v1/product/{product_id}/')
        self.assertEqual(json.loads(gone_product.content)['quantity'], 10)
        self.assertEqual(gone_product.status_code, status.HTTP_200_OK)

        auth_client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_seller}')
        delete_product = auth_client.delete(f'/api/v1/product/{product_id}/')
        self.assertEqual(delete_product.status_code, status.HTTP_204_NO_CONTENT)

        gone_product = auth_client.get(f'/api/v1/product/{product_id}/')
        self.assertEqual(gone_product.status_code, status.HTTP_404_NOT_FOUND)

