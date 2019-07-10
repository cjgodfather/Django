from django.urls import path
from event.views import (
    event_list_view,
    add_to_cart_view,
    event_detail_view,
    CartView,
    delete_tickets_view,
    user_register_view,
    user_login_view,
    user_logout_view,
    checkout_view,
    PaymentView
)

app_name = "event"

urlpatterns = [
    path("", event_list_view, name="list"),
    path("register/", user_register_view, name="register"),
    path("login/", user_login_view, name="login"),
    path("logout/", user_logout_view, name="logout"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/checkout/", checkout_view,  name="checkout"),
    path("cart/checkout/payment/", PaymentView.as_view(),  name="payment"),
    path("cart/delete_ticket/", delete_tickets_view, name="delete_ticket"),
    path("<slug>/add-to-cart/", add_to_cart_view, name="add_to_cart"),
    path("<slug>/", event_detail_view, name="detail"),
]
