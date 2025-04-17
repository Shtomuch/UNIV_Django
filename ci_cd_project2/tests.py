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


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Створюємо фейкове зображення
        fake_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  # мінімальний GIF
            content_type='image/gif'
        )

        self.category = Category.objects.create(
            name='TestCat',
            slug='testcat',
            photo=fake_image
        )

        self.good = Good.objects.create(
            name='TestGood',
            price=10.0,
            count=5,
            category=self.category,
            slug=f"test-good-{uuid.uuid4().hex[:8]}",
            photo=fake_image,
            description='Test description'
        )

    def test_home_view(self):
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x89\x61\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            content_type='image/jpeg'
        )
        Good.objects.create(name='Test Good', price=10, photo=image, category=self.category)

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Good')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)

