from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candle = models.ForeignKey('candles.Candle', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # 1-5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'candle')

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.candle.name}"
