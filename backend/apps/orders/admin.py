from django.contrib import admin

from .models.order import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('candle', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_display_links = ('id',)
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'id')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    actions = ['mark_as_shipped', 'mark_as_delivered']

    @admin.action(description='Отметить как отправленные')
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')

    @admin.action(description='Отметить как доставленные')
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'candle', 'quantity', 'price')
    list_filter = ('order__status',)
    search_fields = ('candle__name', 'order__id')
