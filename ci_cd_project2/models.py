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

# Товари
class Good(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to='goods/')
    description = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    subscribers = models.ManyToManyField(CustomUser, related_name='subscribed_goods', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='goods')

    def __str__(self):
        return self.name

# Повідомлення
class Notification(models.Model):
    message = models.TextField()
    status = models.CharField(max_length=51)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    good = models.ForeignKey(Good, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)

    def __str__(self):
        return self.message


# Замовлення
class Order(models.Model):
    status = models.CharField(max_length=50)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return self.user.get_full_name() + " " + str(self.created_at)

# Позиції в замовленні
class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()
    good = models.ForeignKey(Good, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.good.price * self.quantity

    def __str__(self):
        return self.good.name + " " + str(self.quantity)
