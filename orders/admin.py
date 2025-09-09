from django.contrib import admin
from .models import CartItem, Order, OrderItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "quantity")
    search_fields = ("user__username", "movie__title")
    autocomplete_fields = ("user", "movie")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("movie", "quantity", "price_at_purchase", "subtotal_display")

    def subtotal_display(self, obj):
        return obj.subtotal()
    subtotal_display.short_description = "Subtotal"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at", "total_display")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "id")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at",)

    def total_display(self, obj):
        return obj.total()
    total_display.short_description = "Total"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "movie", "quantity", "price_at_purchase", "subtotal_display")
    autocomplete_fields = ("order", "movie")

    def subtotal_display(self, obj):
        return obj.subtotal()
    subtotal_display.short_description = "Subtotal"
