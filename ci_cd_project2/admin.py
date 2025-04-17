from django.contrib import admin
from .models import CustomUser, Category, Good, Notification, Order, OrderItem

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'first_name', 'last_name', 'address', 'created_at')
    search_fields = ('phone_number',)
    list_editable = ('first_name','last_name', 'phone_number', 'address')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'slug', 'photo', 'created_at')
    search_fields = ('name',)
    list_editable = ('name','photo')

@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'price', 'count', 'category', 'created_at')
    list_filter = ('count', 'category')
    search_fields = ('name',)
    list_editable = ('name', 'price', 'count', 'category')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'status', 'user', 'good', 'created_at')
    list_filter = ('status',)
    search_fields = ('message',)
    list_editable = ('message', 'status', 'user', 'good')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status',)
    list_editable = ('user', 'status')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'good', 'order', 'quantity', 'created_at')
    search_fields = ('good__name',)
    list_editable = ('good', 'order', 'quantity')

