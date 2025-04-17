"""views_commented.py
================================
Цей модуль містить контролери (view‑функції) для веб‑магазину,
реалізованого на Django. Коментарі українською мовою пояснюють логіку
роботи кожної секції коду та її призначення.
"""

# ======================================================================
#                         Імпорт необхідних пакетів
# ======================================================================

import unicodedata  # Нормалізація тексту

from django.contrib import messages  # flash‑повідомлення для користувача
from django.contrib.auth import login, logout  # Аутентифікація користувачів
from django.contrib.auth import update_session_auth_hash  # Зберігає сесію після зміни паролю
from django.contrib.auth.decorators import login_required  # Декоратор перевірки авторизації
from django.contrib.auth.forms import PasswordChangeForm  # Стандартна форма зміни паролю
from django.shortcuts import render, redirect, get_object_or_404  # Шаблонні функції
from django.urls import reverse  # Генерація URL за іменем

from .forms import *  # імпортуємо усі форми поточного застосунку
from .models import *  # імпортуємо всі моделі поточного застосунку


# ----------------------------------------------------------------------
# Допоміжна функція для нормалізації тексту: прибираємо діакритики та
# переводимо у нижній регістр. Використовується у пошуку товарів.
# ----------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """Повертає нормалізований ASCII‑рядок без діакритиків та у нижньому регістрі."""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').lower()


# ======================================================================
#                            View‑функції сайту
# ======================================================================

# ----------------------------------------------------------------------
# Головна сторінка. Показує всі товари та реалізує простий пошук.
# ----------------------------------------------------------------------

def home(request):
    query = request.GET.get('q')  # Параметр пошуку з рядка запиту
    goods = Good.objects.all()  # Витягуємо всі товари

    if query:
        # Шукаємо збіг підрядка у назвах товарів (без врахування регістру)
        normalized_query = query.strip().lower()
        goods = [good for good in goods if normalized_query in good.name.lower()]

    return render(request, 'home.html', {'goods': goods})


# ----------------------------------------------------------------------
# Авторизація користувача (вхід).
# ----------------------------------------------------------------------

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Логінимо користувача
            return redirect('home')  # Переадресація на головну
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


# ----------------------------------------------------------------------
# Реєстрація нового користувача.
# ----------------------------------------------------------------------

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Акаунт створено успішно! Тепер увійдіть.')
            return redirect('login')  # Після успішної реєстрації – на сторінку логіну
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


# ----------------------------------------------------------------------
# Вихід користувача.
# ----------------------------------------------------------------------

def user_logout(request):
    logout(request)
    return redirect('home')  # Повертаємося на головну


# ----------------------------------------------------------------------
# Профіль користувача: історія замовлень та базові дані.
# ----------------------------------------------------------------------

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    return render(request, 'profile.html', {'user': user, 'orders': orders})


# ----------------------------------------------------------------------
# Редагування профілю.
# ----------------------------------------------------------------------

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Профіль успішно оновлений!')
            return redirect('profile')
    else:
        user_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'edit_profile.html', {'user_form': user_form})


# ----------------------------------------------------------------------
# Зміна паролю авторизованим користувачем.
# ----------------------------------------------------------------------

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Щоб сесія не знишилась
            messages.success(request, 'Пароль успішно змінено.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})


# ----------------------------------------------------------------------
# Деталі одного замовлення.
# ----------------------------------------------------------------------

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})


# ======================================================================
#                       Робота з кошиком (Session Cart)
# ======================================================================

# Додаємо товар у кошик (Session‑based).

def add_to_cart(request, good_id):
    good = get_object_or_404(Good, id=good_id)
    cart = request.session.get('cart', {})  # Отримуємо кошик з сесії
    cart[str(good_id)] = cart.get(str(good_id), 0) + 1  # Збільшуємо кількість
    request.session['cart'] = cart  # Зберігаємо кошик у сесії
    return redirect('cart')  # Переходимо до кошика


# Оновлення кількості конкретного товару (збільшити/зменшити).

def update_cart_quantity(request, good_id, action):
    cart = request.session.get('cart', {})
    good_id = str(good_id)
    good = get_object_or_404(Good, id=good_id)

    if good_id in cart:
        if action == 'increase':
            # Не дозволяємо перевищити наявну кількість на складі
            cart[good_id] = min(cart[good_id] + 1, good.count)
        elif action == 'decrease':
            cart[good_id] -= 1
            if cart[good_id] <= 0:
                del cart[good_id]

    request.session['cart'] = cart
    return redirect('cart')


# Видалення товару з кошика повністю.

def remove_from_cart(request, good_id):
    cart = request.session.get('cart', {})
    good_id = str(good_id)
    cart.pop(good_id, None)  # Безпечне видалення
    request.session['cart'] = cart
    return redirect('cart')


# Перегляд кошика.

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for good_id_str, quantity in cart.items():
        try:
            gid = int(good_id_str)
            good = Good.objects.get(id=gid)
        except (ValueError, Good.DoesNotExist):
            # або можна очистити такі записи з cart:
            # del cart[good_id_str]
            continue

        item_total = good.price * quantity
        total += item_total
        cart_items.append({
            'good': good,
            'quantity': quantity,
            'item_total': item_total,
        })

    # За бажанням: оновити сесію без "битих" записів
    request.session['cart'] = {k: v for k, v in cart.items() if Good.objects.filter(id=k).exists()}

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

# ======================================================================
#              Сповіщення про наявність товару та нотифікації
# ======================================================================

from django.contrib.auth.decorators import \
    login_required  # повторний імпорт (можна видалити, але залишено для читабельності)


# Підписка користувача на повідомлення про появу товару.

def notify_availability(request, good_id):
    if not request.user.is_authenticated:
        # Перенаправляємо на логін з параметром next, щоб повернутися після входу
        return redirect(f"{reverse('login')}?next={request.path}")

    good = get_object_or_404(Good, id=good_id)

    # Додаємо користувача до списку підписників, якщо він ще не підписаний.
    if request.user not in good.subscribers.all():
        good.subscribers.add(request.user)
        messages.info(request, f"Ви підписались на сповіщення про {good.name}")
    else:
        messages.warning(request, f"Ви вже підписані на сповіщення про {good.name}")

    return redirect('home')


# Вивід усіх нотифікацій користувача.

@login_required
def notifications(request):
    user_notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': user_notifications})


# ======================================================================
#                           Сторінка товару
# ======================================================================

def good_detail(request, good_id):
    good = get_object_or_404(Good, id=good_id)
    return render(request, 'good_detail.html', {'good': good})


# ======================================================================
#                       Оформлення замовлення (checkout)
# ======================================================================

CustomUser = get_user_model()  # Підтримка кастомної моделі User


def order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Ваш кошик порожній!")
        return redirect('cart')

    if request.method == 'POST':
        # --------------------------------------------------------------
        # 1. Отримуємо або створюємо користувача
        # --------------------------------------------------------------
        if request.user.is_authenticated:
            user = request.user
        else:
            if CustomUser.objects.filter(username=request.POST['username']).exists():
                messages.error(request, "Користувач з таким іменем вже існує.")
                return redirect('order')

            # Створюємо гостя як повноцінного користувача з рандомним паролем
            user = CustomUser.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                phone_number=request.POST['phone_number'],
                address=request.POST['address'],
                password=None  # → Django поставить unusable password
            )

        # --------------------------------------------------------------
        # 2. Створюємо замовлення та додаємо позиції
        # --------------------------------------------------------------
        order = Order.objects.create(user=user, status="Очікується підтвердження")

        for good_id, quantity in cart.items():
            good = get_object_or_404(Good, id=good_id)

            # Актуалізуємо залишок товару
            if good.count >= quantity:
                good.count -= quantity
                good.save()
            else:
                messages.warning(request, f"Товару '{good.name}' залишилось лише {good.count}. Кількість змінено.")
                quantity = good.count
                good.count = 0
                good.save()

            # Додаємо позицію у замовлення, якщо хоч щось залишилося
            if quantity > 0:
                OrderItem.objects.create(order=order, good=good, quantity=quantity)

        # Очищаємо кошик та повідомляємо користувача
        request.session['cart'] = {}
        messages.success(request, "Замовлення успішно оформлено!")
        return redirect('profile' if request.user.is_authenticated else 'home')

    # --------------------------------------------------------------
    # GET‑запит: показуємо форму з поточними товарами у кошику
    # --------------------------------------------------------------
    cart_items = _get_cart_items(cart)
    total = _get_cart_total(cart)
    return render(request, 'order.html', {'cart_items': cart_items, 'total': total})


# ----------------------------------------------------------------------
# Допоміжні функції для розрахунку позицій та сум у кошику
# ----------------------------------------------------------------------

def _get_cart_items(cart):
    return [
        {
            'good': get_object_or_404(Good, id=good_id),
            'quantity': quantity,
            'item_total': get_object_or_404(Good, id=good_id).price * quantity,
        }
        for good_id, quantity in cart.items()
    ]


def _get_cart_total(cart):
    return sum(get_object_or_404(Good, id=good_id).price * quantity for good_id, quantity in cart.items())


# ======================================================================
#                      Категорії та фільтрація товарів
# ======================================================================

def goods_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    goods = Good.objects.filter(category=category)
    return render(request, 'category_goods.html', {'category': category, 'goods': goods})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})
