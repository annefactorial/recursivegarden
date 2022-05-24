import pytest
from django.conf import settings
from backend.core.models import User

from django.urls import reverse

# Comments in the code make the code a record of thoughts


@pytest.mark.django_db
def test_login_success(client):
    # The egg logs into the wobsite
    egg = User.objects.create_user(
        email='email@email.egg',
        password='password')

    # I see the login form wrapper
    login_url = reverse('login')
    response = client.get(login_url)
    assert response.status_code == 200

    # The login form has one htmx component which loads the form, simulated by me getting it manually
    component_url = reverse('login_form_component')
    response = client.get(component_url)
    assert response.status_code == 200

    # I post to the login component with my credentials
    response = client.post(component_url, {
        'username': egg.email,
        'password': 'password',
    })
    # I am redirected to the settings.py LOGIN_REDIRECT_URL
    assert response.status_code == 302
    assert response.url == settings.LOGIN_REDIRECT_URL 


@pytest.mark.django_db
def test_login_failures(client):
    # The egg logs into the wobsite
    egg = User.objects.create_user(
        email='email@email.egg',
        password='password')

    # I see the login form wrapper
    login_url = reverse('login')
    response = client.get(login_url)
    assert response.status_code == 200

    # The login form has one htmx component which loads the form, simulated by me getting it manually
    component_url = reverse('login_form_component')
    response = client.get(component_url)
    assert response.status_code == 200

    # I post to the login component with invalid credentials
    response = client.post(component_url, {
        'username': egg.email,
        'password': 'invalid',
    })
    # I am shown an error message
    assert response.status_code == 200
    assert response.context['form'].errors == {
        '__all__': ['Please enter a correct email and password. Note that both fields may be case-sensitive.']
    }
