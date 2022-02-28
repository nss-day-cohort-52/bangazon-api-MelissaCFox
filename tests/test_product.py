import random
import faker_commerce
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User
from bangazon_api.helpers import STATE_NAMES
from bangazon_api.models import Category
from bangazon_api.models.order import Order
from bangazon_api.models.product import Product
from bangazon_api.models.rating import Rating


class ProductTests(APITestCase):
    def setUp(self):
        """
            set up seed data to use in tests
        """
        call_command('seed_db', user_count=2)
        self.user1 = User.objects.filter(store__isnull=False).first()
        self.token = Token.objects.get(user=self.user1)

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.faker = Faker()
        self.faker.add_provider(faker_commerce.Provider)

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """
        category = Category.objects.first()

        data = {
            "name": self.faker.ecommerce_name(),
            "price": random.randint(50, 1000),
            "description": self.faker.paragraph(),
            "quantity": random.randint(2, 20),
            "location": random.choice(STATE_NAMES),
            "imagePath": "",
            "categoryId": category.id
        }
        response = self.client.post('/api/products', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])


    def test_update_product(self):
        """
        Ensure we can update a product.
        """
        product = Product.objects.first()
        data = {
            "name": product.name,
            "price": product.price,
            "description": self.faker.paragraph(),
            "quantity": product.quantity,
            "location": product.location,
            "imagePath": "",
            "categoryId": product.category.id
        }
        response = self.client.put(f'/api/products/{product.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        product_updated = Product.objects.get(pk=product.id)
        self.assertEqual(product_updated.description, data['description'])

    def test_get_all_products(self):
        """
        Ensure we can get a collection of products.
        """

        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.objects.count())


    def test_delete_product(self):
        """ensure we can delete a product
        """
        category = Category.objects.first()

        product = Product()
        product.name = "Name"
        product.price = 325.5
        product.description = self.faker.paragraph()
        product.quantity = 20
        product.location = "Nashville"
        product.image_path = ""
        product.category_id = category.id
        product.store_id = 1

        product.save()

        url = f'/api/products/{product.id}'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_rate_product(self):
        """ensure we can add a rating to a product
        and the average_rating for the product is also updated
        """
        product = Product.objects.first()
        rating = {
            "score": 1,
            "review": "it was average"
        }

        url = f'/api/products/{product.id}/rate-product'
        response = self.client.post(url, rating, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(f'/api/products/{product.id}')

        total_rating = 0
        for rating in response.data['ratings']:
            total_rating += rating['score']
        average_rating = total_rating / len(response.data['ratings'])

        self.assertEqual(response.data['average_rating'], average_rating)


    def test_add_to_order(self):
        """ensure that adding a product to order adds it to an open
        order and not a closed one"""

        product = Product.objects.first()
        url = f'/api/products/{product.id}/add_to_order'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ## check that the user has an un-completed order
        order = Order.objects.get(
            user=self.user1, completed_on=None, payment_type=None)
        self.assertIsNotNone(order)
