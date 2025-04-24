from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser, Category, Good, Notification, Order, OrderItem

# Inlines for related objects
class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 0
    fields = ('message', 'status', 'good', 'created_at')
    readonly_fields = ('created_at',)

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    fields = ('status', 'created_at')
    readonly_fields = ('created_at',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('good', 'quantity', 'total_price')
    readonly_fields = ('total_price',)

# CustomUser Admin
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'address', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone_number')
    date_hierarchy = 'date_joined'
    fieldsets = (
        ('Credentials', {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Contact Details', {'fields': ('phone_number', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [NotificationInline, OrderInline]
    filter_horizontal = ('groups', 'user_permissions')

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'photo_thumb', 'created_at')
    list_editable = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    readonly_fields = ('photo_thumb', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'slug')}),
        ('Image', {'fields': ('photo', 'photo_thumb')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height: 75px;"/>', obj.photo.url)
        return '-'
    photo_thumb.short_description = 'Preview'

# Good Admin
@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'count', 'category', 'photo_thumb', 'created_at')
    list_editable = ('price', 'count', 'category')
    list_filter = ('category', 'count', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('photo_thumb', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'description')}),
        ('Pricing & Stock', {'fields': ('price', 'count', 'category')}),
        ('Image', {'fields': ('photo', 'photo_thumb')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    filter_horizontal = ('subscribers',)

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height: 75px;"/>', obj.photo.url)
        return '-'
    photo_thumb.short_description = 'Preview'

# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'good', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('message',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('user', 'good')}),
        ('Message', {'fields': ('message', 'status')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'total_items')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    raw_id_fields = ('user',)

    def total_items(self, obj):
        return obj.items.count()
    total_items.short_description = 'Items Count'

# OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'good', 'quantity', 'total_price', 'created_at')
    search_fields = ('good__name', 'order__id')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    raw_id_fields = ('order', 'good')
