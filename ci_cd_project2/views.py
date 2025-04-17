from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
import unicodedata
from django.core.mail import send_mail

from .models import *
from .forms import *
from django.contrib import messages


def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').lower()


def home(request):
    query = request.GET.get('q')
    goods = Good.objects.all()

    if query:
        normalized_query = query.strip().lower()
        goods = [good for good in goods if normalized_query in good.name.lower()]

    return render(request, 'home.html', {'goods': goods})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправлення на домашню сторінку після входу
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Акаунт створено успішно! Тепер увійдіть.')
            return redirect('login')  # або ім’я твого url для логіну
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)  # Вихід з системи
    return redirect('home')  # Перенаправлення на головну сторінку або іншу

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')

    return render(request, 'profile.html', {
        'user': user,
        'orders': orders,
    })


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

    return render(request, 'edit_profile.html', {
        'user_form': user_form
    })


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Щоб не вийшло з системи після зміни пароля
            messages.success(request, 'Пароль успішно змінено.')
            return redirect('profile')  # Або інша сторінка
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

def add_to_cart(request, good_id):
    good = get_object_or_404(Good, id=good_id)
    cart = request.session.get('cart', {})

    cart[str(good_id)] = cart.get(str(good_id), 0) + 1

    request.session['cart'] = cart
    # messages.success(request, f"{good.name} додано у кошик!")

    return redirect('cart')  # 🔄 Переходимо до кошика

def update_cart_quantity(request, good_id, action):
    cart = request.session.get('cart', {})
    good_id = str(good_id)
    good = get_object_or_404(Good, id=good_id)

    if good_id in cart:
        if action == 'increase':
            if cart[good_id] < good.count:
                cart[good_id] += 1
            else:
                cart[good_id] = good.count  # скинути до максимальної доступної кількості
        elif action == 'decrease':
            cart[good_id] -= 1
            if cart[good_id] <= 0:
                del cart[good_id]

    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, good_id):
    cart = request.session.get('cart', {})
    good_id = str(good_id)

    if good_id in cart:
        del cart[good_id]

    request.session['cart'] = cart
    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for good_id, quantity in cart.items():
        good = get_object_or_404(Good, id=good_id)
        item_total = good.price * quantity
        total += item_total
        cart_items.append({
            'good': good,
            'quantity': quantity,
            'item_total': item_total,
        })

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


def notify_availability(request, good_id):

    if not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next={request.path}")

    good = get_object_or_404(Good, id=good_id)

    # Якщо користувач ще не підписаний на цей товар - додаємо в список підписників
    if request.user not in good.subscribers.all():
        good.subscribers.add(request.user)
        messages.info(request, f"Ви підписались на сповіщення про {good.name}")
    else:
        messages.warning(request, f"Ви вже підписані на сповіщення про {good.name}")

    return redirect('home')

from django.contrib.auth.decorators import login_required

@login_required
def notifications(request):
    user_notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': user_notifications})



def good_detail(request, good_id):
    good = get_object_or_404(Good, id=good_id)
    return render(request, 'good_detail.html', {'good': good})


CustomUser = get_user_model()  # для сумісності з кастомним юзером

def order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Ваш кошик порожній!")
        return redirect('cart')

    if request.method == 'POST':
        # Користувач
        if request.user.is_authenticated:
            user = request.user
        else:
            if CustomUser.objects.filter(username=request.POST['username']).exists():
                messages.error(request, "Користувач з таким іменем вже існує.")
                return redirect('order')

            user = CustomUser.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                phone_number=request.POST['phone_number'],
                address=request.POST['address'],
                password=CustomUser.objects.make_random_password()
            )

        # Створення замовлення
        order = Order.objects.create(user=user, status="Очікується підтвердження")

        for good_id, quantity in cart.items():
            good = get_object_or_404(Good, id=good_id)

            # Зменшуємо кількість товару
            if good.count >= quantity:
                good.count -= quantity
                good.save()
            else:
                messages.warning(request, f"Товару '{good.name}' залишилось лише {good.count}. Кількість змінено.")
                quantity = good.count
                good.count = 0
                good.save()

            if quantity > 0:
                OrderItem.objects.create(order=order, good=good, quantity=quantity)

        request.session['cart'] = {}  # Очистити кошик
        messages.success(request, "Замовлення успішно оформлено!")
        return redirect('profile' if request.user.is_authenticated else 'home')

    # GET запит: формування списку товарів
    cart_items = []
    total = 0
    for good_id, quantity in cart.items():
        good = get_object_or_404(Good, id=good_id)
        item_total = good.price * quantity
        total += item_total
        cart_items.append({
            'good': good,
            'quantity': quantity,
            'item_total': item_total,
        })

    return render(request, 'order.html', {
        'cart_items': cart_items,
        'total': total
    })

def _get_cart_items(cart):
    items = []
    for good_id, quantity in cart.items():
        good = get_object_or_404(Good, id=good_id)
        items.append({
            'good': good,
            'quantity': quantity,
            'item_total': good.price * quantity,
        })
    return items

def _get_cart_total(cart):
    total = 0
    for good_id, quantity in cart.items():
        good = get_object_or_404(Good, id=good_id)
        total += good.price * quantity
    return total

def goods_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    goods = Good.objects.filter(category=category)
    return render(request, 'category_goods.html', {
        'category': category,
        'goods': goods
    })

# views.py

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})
