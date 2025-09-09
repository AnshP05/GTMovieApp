from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    # customer
    path("cart/", views.cart, name="cart"),
    path("<int:movie_id>/add/", views.add_to_cart, name="add_to_cart"),
    path("item/<int:item_id>/update/", views.update_quantity, name="update_quantity"),
    path("item/<int:item_id>/remove/", views.remove_from_cart, name="remove_from_cart"),
    path("clear/", views.clear_cart, name="clear_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("mine/", views.my_orders, name="my_orders"),

    # admin-only
    path("admin/", views.orders_admin, name="orders_admin"),
    path("admin/<int:order_id>/update/", views.order_update, name="order_update"),
]
