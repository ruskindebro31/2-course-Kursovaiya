import re
import shutil
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.candles.models import Candle, Category

DEFAULT_SOURCE = Path.home() / 'Desktop' / 'курсовая'

CATALOG = [
    ('Лаванда и мёд', 'Успокаивающий аромат лаванды с нотами мёда', '890.00', 'aromatic', 'spring'),
    ('Ваниль и корица', 'Тёплый зимний аромат ванили и корицы', '750.00', 'aromatic', 'holiday'),
    ('Мраморная свеча', 'Декоративная свеча ручной литьё', '1200.00', 'decorative', 'summer'),
    ('Свеча «Геометрия»', 'Современная форма для минималистичного интерьера', '990.00', 'decorative', 'spring'),
    ('Набор «Уютный вечер»', 'Подарочный набор из трёх ароматических свечей', '2490.00', 'gift-sets', 'holiday'),
    ('Набор «Северные ароматы»', 'Комбинация хвои, цитруса и пряностей', '2690.00', 'gift-sets', 'holiday'),
    ('Сандал и бергамот', 'Мягкий древесно-цитрусовый букет', '820.00', 'aromatic', 'summer'),
    ('Жасминовый сад', 'Нежный цветочный аромат', '910.00', 'aromatic', 'spring'),
    ('Медовый пряник', 'Сладкий аромат праздничной выпечки', '780.00', 'aromatic', 'holiday'),
    ('Кедр и пихта', 'Хвойный зимний аромат', '850.00', 'aromatic', 'holiday'),
    ('Роза и пион', 'Романтичный цветочный микс', '940.00', 'aromatic', 'spring'),
    ('Цитрусовый бриз', 'Освежающий апельсин и лимон', '720.00', 'aromatic', 'summer'),
    ('Кофе и карамель', 'Аромат утреннего капучино', '800.00', 'aromatic', 'summer'),
    ('Мята и эвкалипт', 'Освежающий спа-аромат', '760.00', 'aromatic', 'summer'),
    ('Свеча «Кристалл»', 'Декоративная свеча с фактурой кристалла', '1150.00', 'decorative', 'summer'),
    ('Свеча «Волна»', 'Морская декоративная свеча', '1080.00', 'decorative', 'summer'),
    ('Свеча «Сердце»', 'Подарочная свеча в форме сердца', '980.00', 'decorative', 'spring'),
    ('Амбра и мускус', 'Тёплый восточный аромат', '870.00', 'aromatic', 'spring'),
    ('Набор «Candels Classic»', 'Три бестселлера в фирменной коробке', '2890.00', 'gift-sets', 'holiday'),
    ('Свеча «Пламя»', 'Декоративная свеча с градиентным оформлением', '1020.00', 'decorative', 'summer'),
]

CATEGORY_META = {
    'aromatic': ('Ароматические', 'Свечи с натуральными ароматами'),
    'decorative': ('Декоративные', 'Свечи для интерьера'),
    'gift-sets': ('Подарочные наборы', 'Готовые наборы для подарка'),
}


def photo_sort_key(name: str) -> tuple:
    match = re.search(r'photo_(\d+)', name)
    return (0, int(match.group(1))) if match else (1, name)


class Command(BaseCommand):
    help = 'Создаёт каталог свечей из фотографий папки «курсовая» на рабочем столе'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=Path,
            default=DEFAULT_SOURCE,
            help='Папка с фотографиями свечей',
        )

    def handle(self, *args, **options):
        source: Path = options['source']
        if not source.is_dir():
            self.stderr.write(self.style.ERROR(f'Папка не найдена: {source}'))
            return

        photos = sorted(
            [f for f in source.iterdir() if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}],
            key=lambda p: photo_sort_key(p.name),
        )
        if not photos:
            self.stderr.write(self.style.ERROR(f'В {source} нет изображений'))
            return

        fixtures_dir = Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'images'
        fixtures_dir.mkdir(parents=True, exist_ok=True)

        categories = {}
        for slug, (title, description) in CATEGORY_META.items():
            category, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': title, 'description': description, 'is_active': True},
            )
            categories[slug] = category

        Candle.objects.filter(author__isnull=True).delete()

        count = min(len(photos), len(CATALOG))
        now = timezone.now()
        for index in range(count):
            photo = photos[index]
            name, desc, price, cat_slug, season = CATALOG[index]
            dest_name = f'candle_{index + 1:02d}{photo.suffix.lower()}'
            dest_path = fixtures_dir / dest_name
            shutil.copy2(photo, dest_path)

            candle = Candle.objects.create(
                name=name,
                description=desc,
                price=price,
                category=categories[cat_slug],
                season=season,
                is_published=True,
                created_at=now,
                updated_at=now,
            )
            with dest_path.open('rb') as image_file:
                candle.image.save(dest_name, File(image_file), save=True)
            self.stdout.write(f'  {candle.name} ← {photo.name}')

        self.stdout.write(self.style.SUCCESS(f'Готово: {count} карточек в каталоге'))
