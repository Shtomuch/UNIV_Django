import uuid

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Good, Order, Category
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class CustomUserTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='testpass123', email='test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Snacks')

    def test_product_creation(self):
        product = Good.objects.create(
            name='Chips',
            description='Potato chips',
            price=2.99,
            category=self.category
        )
        self.assertEqual(product.name, 'Chips')
        self.assertEqual(product.price, 2.99)
        self.assertEqual(product.category.name, 'Snacks')

