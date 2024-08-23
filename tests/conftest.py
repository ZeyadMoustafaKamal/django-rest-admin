from django.contrib.auth import get_user_model
from tests.conf.auth import AccessToken

import pytest

User = get_user_model()


@pytest.fixture
def access_token(request):
    user_data = {"username": "user", "password": "password"}
    admin_user = request.node.get_closest_marker("admin_user")

    if admin_user:
        admin_data = {"is_staff": True, "is_superuser": True}
        user_data.update(admin_data)
    user = User.objects.create(**user_data)
    access_token = AccessToken.for_user(user)
    return access_token
