from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notify-availability/<int:good_id>/', views.notify_availability, name='notify_availability'),
    path('login/', views.login_view, name='login'),
    path('good/<int:good_id>/', views.good_detail, name='good_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:good_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:good_id>/', views.update_cart_quantity, {'action': 'increase'}, name='increase_quantity'),
    path('cart/decrease/<int:good_id>/', views.update_cart_quantity, {'action': 'decrease'}, name='decrease_quantity'),
    path('cart/remove/<int:good_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('register/', views.register_view, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('notifications/', views.notifications, name='notifications'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('order/', views.order, name='order'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('category/<slug:slug>/', views.goods_by_category, name='category_goods'),

    path('categories/', views.category_list, name='category_list'),
]