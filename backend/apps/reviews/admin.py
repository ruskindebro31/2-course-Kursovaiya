from django.contrib import admin

from .models.review import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'candle', 'rating', 'created_at')
    list_filter = ('rating',)
