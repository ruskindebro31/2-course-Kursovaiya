from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from apps.candles.models import Candle

DEMO_IMAGES = {
    1: 'lavender.jpg',
    2: 'vanilla.jpg',
    3: 'marble.jpg',
}


class Command(BaseCommand):
    help = 'Прикрепляет демо-изображения к свечам из fixtures/images'

    def handle(self, *args, **options):
        images_dir = Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'images'
        attached = 0
        for pk, filename in DEMO_IMAGES.items():
            candle = Candle.objects.filter(pk=pk).first()
            path = images_dir / filename
            if not candle or not path.exists():
                continue
            with path.open('rb') as image_file:
                candle.image.save(filename, File(image_file), save=True)
            attached += 1
            self.stdout.write(f'  {candle.name}: {filename}')
        self.stdout.write(self.style.SUCCESS(f'Готово: {attached} изображений'))
