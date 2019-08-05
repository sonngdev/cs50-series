from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    path("regular_pizza", views.regular_pizza, name="regular_pizza"),
    path("sicilian_pizza", views.sicilian_pizza, name="sicilian_pizza"),
    path("sub", views.sub, name="sub"),
    path("pasta", views.pasta, name="pasta"),
    path("salad", views.salad, name="salad"),
    path("dinner_platter", views.dinner_platter, name="dinner_platter"),
    path("cart", views.cart, name="cart"),
    path("order", views.order, name="order")
]
