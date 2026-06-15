import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_candles_list_public():
    client = APIClient()
    response = client.get('/api/candles/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_login_create_candle():
    client = APIClient()
    client.post('/api/auth/register/', {
        'username': 'author1',
        'email': 'author1@example.com',
        'first_name': 'Author',
        'last_name': 'One',
        'password': 'securepass123',
        'password_confirm': 'securepass123',
    })
    login = client.post('/api/auth/login/', {
        'email': 'author1@example.com',
        'password': 'securepass123',
    })
    assert login.status_code == 200
    token = login.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    from apps.candles.models import Category
    cat = Category.objects.create(name='Test', slug='test', description='d')
    create = client.post('/api/candles/', {
        'name': 'My Candle',
        'description': 'Desc',
        'price': '500.00',
        'category': cat.id,
        'is_published': True,
    })
    assert create.status_code == 201
    assert create.data['author_name'] == 'author1'

    mine = client.get('/api/candles/mine/')
    assert mine.status_code == 200
    assert len(mine.data['results']) == 1


@pytest.mark.django_db
def test_favorites_toggle():
    client = APIClient()
    client.post('/api/auth/register/', {
        'username': 'favuser',
        'email': 'fav@example.com',
        'first_name': 'F',
        'last_name': 'U',
        'password': 'securepass123',
        'password_confirm': 'securepass123',
    })
    login = client.post('/api/auth/login/', {'email': 'fav@example.com', 'password': 'securepass123'})
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {login.data["access"]}')

    from apps.candles.models import Category, Candle
    cat = Category.objects.create(name='C', slug='c', description='')
    candle = Candle.objects.create(name='X', description='d', price=100, category=cat)

    on = client.post('/api/favorites/toggle/', {'candle': candle.id})
    assert on.status_code == 201
    assert on.data['favorited'] is True

    off = client.post('/api/favorites/toggle/', {'candle': candle.id})
    assert off.data['favorited'] is False
