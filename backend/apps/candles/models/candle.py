from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, default='category')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Candle(models.Model):
    SEASON_SPRING = 'spring'
    SEASON_SUMMER = 'summer'
    SEASON_HOLIDAY = 'holiday'
    SEASON_CHOICES = [
        (SEASON_SPRING, 'Весенние'),
        (SEASON_SUMMER, 'Летние'),
        (SEASON_HOLIDAY, 'Праздничные'),
    ]

    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='candles')
    season = models.CharField(
        max_length=20,
        choices=SEASON_CHOICES,
        default=SEASON_SPRING,
        db_index=True,
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='candles',
    )
    image = models.ImageField(upload_to='candles/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
