from django.db import models
from django.contrib.auth.models import AbstractUser

# Інформація про користувача
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=13)
    address = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name()

class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField("categories/")

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
