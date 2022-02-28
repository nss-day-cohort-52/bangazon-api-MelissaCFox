from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models import Order, Product
from bangazon_api.models.payment_type import PaymentType


class OrderTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)

        self.user2 = User.objects.filter(store=None).last()
        product = Product.objects.get(pk=1)

        self.order1 = Order.objects.create(
            user=self.user1
        )

        self.order1.products.add(product)

        self.order2 = Order.objects.create(
            user=self.user2
        )

        self.order2.products.add(product)

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.payment_type = PaymentType.objects.create(
            merchant_name = "Visa 13 digit",
            acct_number = 123467890123,
            customer_id = 1
        )

    # def test_list_orders(self):
    #     # ! NEED TO FIX THIS ONE - response data should only have a length of 1?
    #     """The orders list should return a list of orders for the logged in user"""
    #     response = self.client.get('/api/orders')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)


    def test_delete_order(self):
        """ ensure you can delete an order"""
        response = self.client.delete(f'/api/orders/{self.order1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_complete_order(self):
        """ensure you can update an order as complete by adding a payment_type
        """
        data = {
            "paymentTypeId": self.payment_type.id
        }

        response = self.client.put(f'/api/orders/{self.order1.id}/complete', data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        order = Order.objects.get(pk = self.order1.id)

        self.assertEqual(order.payment_type_id, data['paymentTypeId'])
