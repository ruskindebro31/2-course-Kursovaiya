from django.contrib import admin

from .models.notification import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'is_read', 'created_at')
    list_display_links = ('id',)
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)
