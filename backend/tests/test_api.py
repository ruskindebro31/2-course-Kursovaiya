import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_candles_list_public():
    client = APIClient()
    response = client.get('/api/candles/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_and_login():
    client = APIClient()
    register = client.post('/api/auth/register/', {
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'securepass123',
        'password_confirm': 'securepass123',
    })
    assert register.status_code == 201
    login = client.post('/api/auth/login/', {
        'email': 'test@example.com',
        'password': 'securepass123',
    })
    assert login.status_code == 200
    assert 'access' in login.data
