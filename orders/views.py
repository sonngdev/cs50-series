from django.contrib.auth import authenticate, login, logout, models
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Cart, CartItem, Order, RegularPizza, SicilianPizza, Topping, Sub, SubAddon, Pasta, Salad, DinnerPlatter

# Create your views here.
def index(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'auth/login.html', {'message': None})

    try:
        cart = user.cart
    except:
        cart = Cart.objects.create(user=user)

    context = {
        'cart_size': cart.items.filter(status='in_cart', parent=None).count(),
        'regular_pizzas': RegularPizza.objects.all(),
        'sicilian_pizzas': SicilianPizza.objects.all(),
        'toppings': Topping.objects.all(),
        'subs': Sub.objects.all(),
        'pastas': Pasta.objects.all(),
        'salads': Salad.objects.all(),
        'dinner_platters': DinnerPlatter.objects.all(),
    }
    return render(request, 'orders/index.html', context)

def login_view(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html', {'message': None})

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is None:
        return render(request, 'auth/login.html', {'message': 'Invalid credentials.'})

    login(request, user)
    return HttpResponseRedirect(reverse('index'))

def logout_view(request):
    logout(request)
    return render(request, 'auth/login.html', {'message': 'Logged out.'})

def signup_view(request):
    if request.method == 'GET':
        return render(request, 'auth/signup.html', {'message': None})

    username = request.POST['username']
    email    = request.POST['email']
    password = request.POST['password']

    try:
        user = models.User.objects.create_user(username, email, password)
    except IntegrityError:
        return render(request, 'auth/signup.html', {'message': 'Username taken.'})

    login(request, user)
    return HttpResponseRedirect(reverse('index'))

def regular_pizza(request):
    name = request.POST['name']
    size = request.POST['size']
    toppings = request.POST.getlist('toppings')

    cart = request.user.cart
    rp = RegularPizza.objects.get(name=name)
    cart_item = CartItem(
        cart=cart,
        product_object_id=rp.pk,
        product_content_type=ContentType.objects.get_for_model(rp),
    )
    if size == 'small':
        cart_item.size = 'small'
        cart_item.price = rp.small_price
    elif size == 'large':
        cart_item.size = 'large'
        cart_item.price = rp.large_price
    cart_item.save()

    for t in toppings:
        topping = Topping.objects.get(name=t)
        CartItem.objects.create(
            cart=cart,
            price=0,
            product_object_id=topping.pk,
            product_content_type=ContentType.objects.get_for_model(topping),
            parent=cart_item,
        )

    return HttpResponseRedirect(reverse('index'))

def sicilian_pizza(request):
    name = request.POST['name']
    size = request.POST['size']
    items = request.POST.getlist('items')

    cart = request.user.cart
    sp = SicilianPizza.objects.get(name=name)
    cart_item = CartItem(
        cart=cart,
        product_object_id=sp.pk,
        product_content_type=ContentType.objects.get_for_model(sp),
    )
    if size == 'small':
        cart_item.size = 'small'
        cart_item.price = sp.small_price
    elif size == 'large':
        cart_item.size = 'large'
        cart_item.price = sp.large_price
    cart_item.save()

    for i in items:
        topping = Topping.objects.get(name=i)
        CartItem.objects.create(
            cart=cart,
            price=0,
            product_object_id=topping.pk,
            product_content_type=ContentType.objects.get_for_model(topping),
            parent=cart_item,
        )

    return HttpResponseRedirect(reverse('index'))

def sub(request):
    name = request.POST['name']
    size = request.POST['size']
    addons = request.POST.getlist('addons')

    cart = request.user.cart
    sub = Sub.objects.get(name=name)
    cart_item = CartItem(
        cart=cart,
        product_object_id=sub.pk,
        product_content_type=ContentType.objects.get_for_model(sub),
    )
    if size == 'small':
        cart_item.size = 'small'
        cart_item.price = sub.small_price
    elif size == 'large':
        cart_item.size = 'large'
        cart_item.price = sub.large_price
    cart_item.save()

    for addon in addons:
        sub_addon = SubAddon.objects.get(sub=sub, name=addon)
        CartItem.objects.create(
            cart=cart,
            price=sub_addon.price,
            product_object_id=sub_addon.pk,
            product_content_type=ContentType.objects.get_for_model(sub_addon),
            parent=cart_item,
        )

    return HttpResponseRedirect(reverse('index'))

def pasta(request):
    name = request.POST['name']
    cart = request.user.cart
    pasta = Pasta.objects.get(name=name)
    cart_item = CartItem.objects.create(
        cart=cart,
        price=pasta.price,
        product_object_id=pasta.pk,
        product_content_type=ContentType.objects.get_for_model(pasta),
    )

    return HttpResponseRedirect(reverse('index'))

def salad(request):
    name = request.POST['name']
    cart = request.user.cart
    salad = Salad.objects.get(name=name)
    cart_item = CartItem.objects.create(
        cart=cart,
        price=salad.price,
        product_object_id=salad.pk,
        product_content_type=ContentType.objects.get_for_model(salad),
    )

    return HttpResponseRedirect(reverse('index'))

def dinner_platter(request):
    name = request.POST['name']
    size = request.POST['size']

    cart = request.user.cart
    dp = DinnerPlatter.objects.get(name=name)
    cart_item = CartItem(
        cart=cart,
        product_object_id=dp.pk,
        product_content_type=ContentType.objects.get_for_model(dp),
    )
    if size == 'small':
        cart_item.size = 'small'
        cart_item.price = dp.small_price
    elif size == 'large':
        cart_item.size = 'large'
        cart_item.price = dp.large_price
    cart_item.save();

    return HttpResponseRedirect(reverse('index'))

def cart(request):
    user = request.user

    try:
        cart = user.cart
    except:
        cart = Cart.objects.create(user=user)

    all_items = cart.items.filter(status='in_cart').all()
    total = sum(item.price for item in all_items)
    items = all_items.filter(parent=None).all()

    context = {
        'cart_size': len(items),
        'items': items,
        'total': total,
    }
    return render(request, 'orders/cart.html', context)

def order(request):
    user = request.user
    items = user.cart.items.filter(status='in_cart').all()
    total = sum(item.price for item in items)
    order = Order.objects.create(user=user, total=total)
    items.update(status='ordered', order=order)

    return HttpResponseRedirect(reverse('index'))

def orders(request):
    orders = {}
    for o in Order.objects.all():
        items = {}
        parents = o.items.filter(status='ordered', parent=None).all()
        for p in parents:
            items[p] = p.children.all()
        orders[o] = items

    cart_size = request.user.cart.items.filter(status='in_cart', parent=None).count()

    context = {
        'cart_size': cart_size,
        'orders': orders,
    }
    return render(request, 'orders/orders.html', context)
