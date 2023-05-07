import pytest
from django.contrib.auth.hashers import check_password
from django.test import Client
from django.urls import reverse
import django
from django.contrib.auth import get_user_model

django.setup()

@pytest.mark.django_db
def test_login_view_get(client):
    response = client.get(reverse('account_login'))
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_login_view_post_invalid_form(client):
    response = client.post(reverse('account_login'), {
        'sign-up': True,
        'email': 'test@example.com',
        'password1': 'testpassword',
        'password2': 'notmatchingpassword'
    })
    assert response.status_code == 302
    assert response.url == "/"

@pytest.mark.django_db
def test_login_view_post_valid_form(client):
    response = client.post(reverse('account_login'), {
        'sign-up': True,
        'email': 'test@example.com',
        'password1': 'testpassword',
        'password2': 'testpassword'
    })
    assert response.status_code == 302
    assert response.url == "/"
    user = get_user_model().objects.filter(email='test@example.com').first()
    assert user is not None

@pytest.mark.django_db
def test_login_view_post_invalid_credentials(client):
    response = client.get(reverse('account_login'), {
        'sign-in': True,
        'email': 'test@example.com',
        'pswd': 'wrongpassword'
    })
    assert response.status_code == 302
    assert response.url == "/"

@pytest.mark.django_db
def test_login_view_post_valid_credentials(client, user):
    response = client.get(reverse('account_login'), {
        'sign-in': True,
        'email': 'test@example.com',
        'pswd': 'testpassword'
    })
    assert response.status_code == 302
    assert '/dashboard' in response.url

@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(email='test@example.com', password='testpassword')

@pytest.mark.django_db
def test_logout_view(client, user):
    client.login(email='test@example.com', password='testpassword')
    response = client.get(reverse('account_logout'))
    assert response.status_code == 302
    assert response.url == "/"

@pytest.mark.django_db
def test_home_view_not_authenticated(client):
    response = client.get(reverse('home'))
    assert response.status_code == 403

@pytest.mark.django_db
def test_home_view_authenticated(client, user):
    client.login(email='test@example.com', password='testpassword')
    response = client.get(reverse('home'))
    assert response.status_code == 200
