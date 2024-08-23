from rest_admin.site import site
from django.contrib.admin.exceptions import AlreadyRegistered, NotRegistered
from django.core.exceptions import ImproperlyConfigured


from tests.models import Model

import pytest


class Foo(Model):
    pass


def test_register():
    try:
        site.register(Foo)
    finally:
        site.unregister(Foo)


def test_rais_for_already_registered():
    site.register(Foo)
    with pytest.raises(AlreadyRegistered):
        site.register(Foo)
    site.unregister(Foo)


def test_register_none_model():
    with pytest.raises(ImproperlyConfigured):
        site.register(str)


def test_register_abstract_model():
    with pytest.raises(ImproperlyConfigured):
        site.register(Model)  # The base class for all models


def test_unregister():
    site.register(Foo)
    site.unregister(Foo)


def test_raise_for_not_registered():
    with pytest.raises(NotRegistered):
        site.unregister(Foo)


def test_is_registered():
    site.register(Foo)
    assert site.is_registered(Foo)
