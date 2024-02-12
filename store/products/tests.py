from http import HTTPStatus

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from products.models import Basket, Product, ProductCategory
from users.models import User


class IndexViewTestCase(TestCase):
    
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')
        
        
class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:2]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )
        
        
class BasketAddTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def setUp(self):
        self.path = reverse('users:register')
        self.data = {
            'first_name': 'qwerty',
            'last_name': 'qwerty123',
            'username': 'qwerty1234',
            'email': 'qwerty123qwe@erty.com',
            'password1': '12345678qwezxC',
            'password2': '12345678qwezxC',
        }
    
    def test_basket_add(self):
        self.client.post(self.path, self.data)
        user = User.objects.first()
        product = Product.objects.first()
        Basket.objects.create(user=user, product=product, quantity=1)
        basket = Basket.objects.first()
        print(basket)

        self.assertEqual(basket.quantity, 1)


        

