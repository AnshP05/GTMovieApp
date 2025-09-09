from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django import forms

from movies.models import Movie
from .models import CartItem, Order, OrderItem


# -------------------
# Customer cart flows
# -------------------

@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user).select_related("movie")
    total = sum(i.line_total() for i in items)
    return render(request, "orders/cart.html", {"items": items, "total": total})


@login_required
def add_to_cart(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        qty_raw = request.POST.get("quantity", "1")
        try:
            qty = max(1, int(qty_raw))
        except ValueError:
            qty = 1
        item, created = CartItem.objects.get_or_create(user=request.user, movie=movie)
        item.quantity = item.quantity + qty if not created else qty
        item.save()
        messages.success(request, f"Added {qty} × {movie.title} to cart.")
    return redirect("movies:movie_detail", pk=movie_id)


@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    if request.method == "POST":
        qty_raw = request.POST.get("quantity", "1")
        try:
            qty = max(1, int(qty_raw))
        except ValueError:
            qty = 1
        item.quantity = qty
        item.save()
        messages.success(request, "Quantity updated.")
    return redirect("orders:cart")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    if request.method == "POST":
        item.delete()
        messages.info(request, "Item removed from cart.")
    return redirect("orders:cart")


@login_required
def clear_cart(request):
    if request.method == "POST":
        CartItem.objects.filter(user=request.user).delete()
        messages.info(request, "Cart cleared.")
    return redirect("orders:cart")


@login_required
def checkout(request):
    items = list(CartItem.objects.filter(user=request.user).select_related("movie"))
    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect("orders:cart")

    if request.method == "POST":
        order = Order.objects.create(user=request.user)  # status defaults to pending
        for i in items:
            OrderItem.objects.create(
                order=order,
                movie=i.movie,
                quantity=i.quantity,
                price_at_purchase=i.movie.price,
            )
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, f"Order #{order.pk} placed.")
        return redirect("orders:my_orders")

    total = sum(i.line_total() for i in items)
    return render(request, "orders/checkout.html", {"items": items, "total": total})


@login_required
def my_orders(request):
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related("items__movie")
        .order_by("-created_at")
    )
    return render(request, "orders/my_orders.html", {"orders": orders})


# -------------------
# Admin (staff only)
# -------------------

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]


@staff_member_required
def orders_admin(request):
    q = Order.objects.all().select_related("user").prefetch_related("items__movie").order_by("-created_at")
    status = request.GET.get("status")
    if status:
        q = q.filter(status=status)
    return render(request, "orders/admin_orders.html", {"orders": q})


@staff_member_required
def order_update(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Order #{order.pk} updated.")
            return redirect("orders:orders_admin")
    else:
        form = OrderUpdateForm(instance=order)
    return render(request, "orders/admin_order_update.html", {"form": form, "order": order})
