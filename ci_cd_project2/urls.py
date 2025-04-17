"""urls_commented.py
================================
Файл маршрутизації Django‑застосунку. Коментарі українською мовою пояснюють
призначення кожного шляху (URL pattern) та аргументів, які передаються у
view‑функції.
"""

from django.urls import path               # Функція «path» описує шаблони URL
from . import views                        # Імпортуємо view‑функції поточного застосунку

# ======================================================================
#                         Перелік маршрутів сайту
# ======================================================================

urlpatterns = [
    # ------------------------------------------------------------------
    # Головна сторінка магазину.
    #   URL:   /
    #   View:  views.home
    #   Name:  home  – використовується у {% url 'home' %}
    # ------------------------------------------------------------------
    path('', views.home, name='home'),

    # ------------------------------------------------------------------
    # Підписка на сповіщення про появу товару у продажу.
    #   good_id – первинний ключ товару.
    # ------------------------------------------------------------------
    path('notify-availability/<int:good_id>/', views.notify_availability, name='notify_availability'),

    # Аутентифікація та реєстрація ------------------------------------------------
    path('login/',     views.login_view,   name='login'),        # Сторінка входу
    path('register/',  views.register_view, name='register'),    # Сторінка реєстрації
    path('logout/',    views.user_logout,  name='logout'),       # Вихід користувача

    # ------------------------------------------------------------------
    # Перегляд конкретного товару.
    # ------------------------------------------------------------------
    path('good/<int:good_id>/', views.good_detail, name='good_detail'),

    # ------------------------------------------------------------------
    # Кошик та повʼязані дії.
    # ------------------------------------------------------------------
    path('cart/', views.cart_view, name='cart'),                       # Перегляд кошика
    path('add-to-cart/<int:good_id>/', views.add_to_cart, name='add_to_cart'),

    # Зміна кількості товару у кошику (increase / decrease).
    # Використовуємо додатковий словник kwargs, щоб передати дію у view.
    path('cart/increase/<int:good_id>/', views.update_cart_quantity, {'action': 'increase'}, name='increase_quantity'),
    path('cart/decrease/<int:good_id>/', views.update_cart_quantity, {'action': 'decrease'}, name='decrease_quantity'),

    # Видалення товару з кошика повністю.
    path('cart/remove/<int:good_id>/', views.remove_from_cart, name='remove_from_cart'),

    # ------------------------------------------------------------------
    # Особистий кабінет користувача.
    # ------------------------------------------------------------------
    path('profile/',         views.profile,             name='profile'),
    path('edit-profile/',    views.edit_profile,        name='edit_profile'),
    path('change-password/', views.change_password_view, name='change_password'),

    # Деталі замовлення (history)
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    # Оформлення нового замовлення (checkout)
    path('order/', views.order, name='order'),

    # Сторінка сповіщень користувача
    path('notifications/', views.notifications, name='notifications'),

    # ------------------------------------------------------------------
    # Фільтрація товарів за категорією.
    #   slug – читабельний ідентифікатор категорії.
    # ------------------------------------------------------------------
    path('category/<slug:slug>/', views.goods_by_category, name='category_goods'),

    # Список усіх категорій
    path('categories/', views.category_list, name='category_list'),
]
