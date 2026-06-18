from django.contrib import admin

from .models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('timestamp',)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'participants_list')
    list_display_links = ('id',)
    filter_horizontal = ('participants',)
    readonly_fields = ('created_at',)
    inlines = [MessageInline]

    @admin.display(description='Участники')
    def participants_list(self, obj):
        return ', '.join(u.username for u in obj.participants.all())


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'text_short', 'is_read', 'timestamp')
    list_display_links = ('id',)
    list_filter = ('is_read', 'timestamp')
    search_fields = ('text', 'sender__username')
    list_editable = ('is_read',)
    readonly_fields = ('timestamp',)

    @admin.display(description='Текст')
    def text_short(self, obj):
        return obj.text[:50] + ('…' if len(obj.text) > 50 else '')
