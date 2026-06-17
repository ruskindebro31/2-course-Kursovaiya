#!/usr/bin/env python3
"""Генерация скриншотов интерфейса Candels для Приложения Б."""

from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("pip install Pillow")

OUT = Path(__file__).resolve().parent / "images" / "screenshots"
W, H = 1280, 800
BG = "#faf8f5"
ACCENT = "#8b5a2b"
TEXT = "#2c2416"
CARD = "#ffffff"
BORDER = "#e8dfd0"
BADGE = "#c45c26"


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "arial.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def base(title: str) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 56], fill=CARD, outline=BORDER)
    d.text((24, 16), "Candels", fill=ACCENT, font=font(28, True))
    for i, label in enumerate(["Каталог", "Корзина", "Заказы", "Профиль", "Войти"]):
        d.text((200 + i * 130, 20), label, fill=TEXT, font=font(16))
    d.text((24, 72), title, fill=TEXT, font=font(22, True))
    return img


def save(img: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    img.save(path, "PNG")
    print(f"  {path.name}")


def shot_home():
    img = base("Главная страница")
    d = ImageDraw.Draw(img)
    d.rectangle([200, 200, 1080, 520], fill=CARD, outline=BORDER, width=2)
    d.text((420, 280), "Candels", fill=ACCENT, font=font(48, True))
    d.text((340, 360), "Интернет-магазин свечей ручной работы", fill=TEXT, font=font(22))
    d.rectangle([500, 420, 720, 470], fill=ACCENT)
    d.text((530, 432), "Смотреть каталог", fill="white", font=font(20))
    save(img, "01_home.png")


def shot_catalog():
    img = base("Каталог свечей")
    d = ImageDraw.Draw(img)
    d.text((24, 110), "Поиск: лаванда", fill=TEXT, font=font(16))
    x0, y0 = 24, 150
    for row in range(2):
        for col in range(4):
            x, y = x0 + col * 300, y0 + row * 280
            d.rectangle([x, y, x + 280, y + 250], fill=CARD, outline=BORDER)
            d.rectangle([x + 10, y + 10, x + 270, y + 150], fill="#f3e8d8")
            names = ["Лавандовая", "Ванильная", "Сосновая", "Медовая",
                     "Розовая", "Корица", "Океан", "Ягодная"]
            idx = row * 4 + col
            d.text((x + 15, y + 165), names[idx], fill=TEXT, font=font(16))
            d.text((x + 15, y + 195), f"{450 + idx * 50} ₽", fill=ACCENT, font=font(18, True))
    save(img, "02_catalog.png")


def shot_detail():
    img = base("Карточка свечи")
    d = ImageDraw.Draw(img)
    d.rectangle([24, 120, 500, 500], fill="#f3e8d8", outline=BORDER)
    d.text((540, 130), "Лавандовая свеча ручной работы", fill=TEXT, font=font(26, True))
    d.text((540, 180), "650 ₽", fill=ACCENT, font=font(32, True))
    d.text((540, 240), "Ароматическая свеча из соевого воска.", fill=TEXT, font=font(18))
    d.text((540, 280), "Автор: master_candle", fill=TEXT, font=font(16))
    d.rectangle([540, 330, 720, 380], fill=ACCENT)
    d.text((570, 345), "В корзину", fill="white", font=font(18))
    d.text((760, 345), "♥ Избранное", fill=BADGE, font=font(18))
    d.text((24, 530), "Отзывы (WebSocket)", fill=TEXT, font=font(20, True))
    d.text((24, 570), "★★★★★  Отличный аромат! — user1", fill=TEXT, font=font(16))
    save(img, "03_candle_detail.png")


def shot_cart():
    img = base("Корзина")
    d = ImageDraw.Draw(img)
    items = [("Лавандовая свеча", 650, 2), ("Ванильная свеча", 500, 1)]
    y = 130
    for name, price, qty in items:
        d.rectangle([24, y, 1200, y + 80], fill=CARD, outline=BORDER)
        d.text((40, y + 25), f"{name}  ×{qty}", fill=TEXT, font=font(18))
        d.text((1000, y + 25), f"{price * qty} ₽", fill=ACCENT, font=font(18, True))
        y += 95
    d.text((900, 350), "Итого: 1800 ₽", fill=TEXT, font=font(22, True))
    d.rectangle([900, 390, 1150, 440], fill=ACCENT)
    d.text((930, 403), "Оформить заказ", fill="white", font=font(18))
    save(img, "04_cart.png")


def shot_orders():
    img = base("Мои заказы")
    d = ImageDraw.Draw(img)
    orders = ["#12 — 1800 ₽ — confirmed", "#11 — 650 ₽ — delivered"]
    y = 130
    for o in orders:
        d.rectangle([24, y, 1200, y + 70], fill=CARD, outline=BORDER)
        d.text((40, y + 22), o, fill=TEXT, font=font(18))
        y += 85
    save(img, "05_orders.png")


def shot_login():
    img = base("Вход в систему")
    d = ImageDraw.Draw(img)
    d.rectangle([400, 180, 880, 520], fill=CARD, outline=BORDER, width=2)
    d.text((560, 210), "Вход", fill=TEXT, font=font(28, True))
    d.text((430, 280), "Email:", fill=TEXT, font=font(18))
    d.rectangle([430, 310, 850, 350], outline=BORDER)
    d.text((440, 318), "user@example.com", fill="#888", font=font(16))
    d.text((430, 370), "Пароль:", fill=TEXT, font=font(18))
    d.rectangle([430, 400, 850, 440], outline=BORDER)
    d.rectangle([430, 460, 850, 500], fill=ACCENT)
    d.text((600, 472), "Войти", fill="white", font=font(18))
    save(img, "06_login.png")


def shot_register():
    img = base("Регистрация")
    d = ImageDraw.Draw(img)
    d.rectangle([380, 150, 900, 560], fill=CARD, outline=BORDER, width=2)
    d.text((530, 175), "Регистрация", fill=TEXT, font=font(26, True))
    for i, label in enumerate(["Имя пользователя", "Email", "Пароль", "Повтор пароля"]):
        y = 230 + i * 70
        d.text((410, y), label, fill=TEXT, font=font(16))
        d.rectangle([410, y + 22, 870, y + 55], outline=BORDER)
    d.rectangle([410, 500, 870, 540], fill=ACCENT)
    d.text((560, 512), "Зарегистрироваться", fill="white", font=font(18))
    save(img, "07_register.png")


def shot_profile():
    img = base("Профиль пользователя")
    d = ImageDraw.Draw(img)
    d.rectangle([24, 120, 600, 400], fill=CARD, outline=BORDER)
    d.text((40, 140), "Рашевский Роман", fill=TEXT, font=font(24, True))
    d.text((40, 190), "Email: user@example.com", fill=TEXT, font=font(18))
    d.text((40, 230), "Телефон: +7 900 000-00-00", fill=TEXT, font=font(18))
    d.text((40, 270), "О себе: Люблю handmade свечи", fill=TEXT, font=font(18))
    save(img, "08_profile.png")


def shot_my_candles():
    img = base("Мои свечи")
    d = ImageDraw.Draw(img)
    d.rectangle([1000, 110, 1200, 150], fill=ACCENT)
    d.text((1020, 118), "+ Добавить", fill="white", font=font(16))
    y = 170
    for name, price in [("Лавандовая", "650"), ("Медовая", "550")]:
        d.rectangle([24, y, 1200, y + 70], fill=CARD, outline=BORDER)
        d.text((40, y + 22), f"{name} — {price} ₽ — опубликовано", fill=TEXT, font=font(18))
        y += 85
    save(img, "09_my_candles.png")


def shot_favorites():
    img = base("Избранное")
    d = ImageDraw.Draw(img)
    x, y = 24, 130
    for i, name in enumerate(["Лавандовая", "Розовая", "Корица"]):
        d.rectangle([x + i * 310, y, x + i * 310 + 290, y + 220], fill=CARD, outline=BORDER)
        d.rectangle([x + i * 310 + 10, y + 10, x + i * 310 + 280, y + 140], fill="#f3e8d8")
        d.text((x + i * 310 + 15, y + 155), name, fill=TEXT, font=font(16))
        d.text((x + i * 310 + 240, y + 155), "♥", fill=BADGE, font=font(20))
    save(img, "10_favorites.png")


def shot_swagger():
    img = Image.new("RGB", (W, H), "#1b1b1b")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 50], fill="#2d2d2d")
    d.text((24, 14), "Candels API — Swagger UI", fill="#61affe", font=font(22, True))
    d.text((24, 70), "GET /api/candles/ — Список свечей", fill="#49cc90", font=font(18))
    d.text((24, 110), "POST /api/auth/login/ — JWT вход", fill="#fca130", font=font(18))
    d.text((24, 150), "POST /api/orders/ — Оформление заказа", fill="#fca130", font=font(18))
    d.text((24, 190), "WS /ws/notifications/{user_id}/ — WebSocket", fill="#9b59b6", font=font(18))
    d.text((24, 250), "OpenAPI 3.0 — drf-spectacular", fill="#aaaaaa", font=font(16))
    d.rectangle([24, 300, 1250, 750], outline="#444444")
    d.text((40, 320), '{ "name": "Лавандовая свеча", "price": "650.00" }', fill="#98c379", font=font(16))
    save(img, "11_swagger.png")


def main() -> None:
    print(f"Screenshots -> {OUT}")
    shot_home()
    shot_catalog()
    shot_detail()
    shot_cart()
    shot_orders()
    shot_login()
    shot_register()
    shot_profile()
    shot_my_candles()
    shot_favorites()
    shot_swagger()
    print(f"Created {len(list(OUT.glob('*.png')))} files")


if __name__ == "__main__":
    main()
