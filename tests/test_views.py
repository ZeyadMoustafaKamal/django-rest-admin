from django.urls import reverse
from rest_admin.site import site

import pytest

from .models import Model

@pytest.mark.django_db
def test_not_allowed(client, access_token):
    url = reverse("rest_admin:index")
    res = client.get(url)
    assert res.status_code == 403
    res = client.get(url, headers=access_token.auth_header) 
    assert res.status_code == 403

@pytest.mark.admin_user
@pytest.mark.django_db
def test_get_apps(client, access_token):
    class Bar(Model):
        pass

    site.register(Bar)

    url = reverse("rest_admin:index")
    res = client.get(url, headers=access_token.auth_header)
    assert res.status_code == 200
    data = {"apps": {"tests": {"models": [{"model_name": "Bars"}]}}}
    assert res.data == data
