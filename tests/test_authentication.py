import pytest
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
import django
django.setup()

@pytest.fixture
def create_user(db):
    """
    Create a User object
    """
    return User.objects.create_user(
        username = 'testuser',
        password = 'testpass'
    )


def test_registration(create_user):
    """
    Test whether a user was added to the user databse
    """
    client = Client()
    assert User.objects.filter(username = 'testuser').exists()


def test_login(create_user):
    """
    Test whether the user can log into their account
    - if user exists in the database, check whether the user entered their account
    - if the user is not in the databse, check whether the view returned to the login screen
    """
    
    client = Client()
    response_success = client.get(reverse('account_login') + f'?sign-in=1&username=testuser&pswd=testpass')
    response_fail = client.get(reverse('account_login') + f'?sign-in=1&username=notexists&pswd=notexists')

    assert response_success.status_code == 302
    assert response_success.url == reverse('home')
    assert response_fail.url == reverse('account_login')
