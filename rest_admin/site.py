from django.contrib.admin.exceptions import NotRegistered, AlreadyRegistered
from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.utils.text import capfirst

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_admin.options import ModelAdmin


class AdminSite:
    def __init__(self):
        self._registry = {}

    def register(self, model, model_admin=None):
        model_admin = model_admin or ModelAdmin
        if not isinstance(model, ModelBase):
            raise ImproperlyConfigured(
                "Expected to get Model got %s" % model.__class__.__name__
            )
        if model._meta.abstract:
            raise ImproperlyConfigured("You can't use abstracted models")
        if self.is_registered(model):
            raise AlreadyRegistered(
                "The model %s already reigtered" % model.__class__.__name__
            )
        if not model._meta.swapped:
            self._registry[model] = model_admin

    def unregister(self, model):
        try:
            del self._registry[model]
        except KeyError:
            raise NotRegistered(
                "The model %s is not registered" % model.__name__
            )

    def is_registered(self, model):
        return model in self._registry

    def has_permission(self, request):
        """
        ٌReturn True of the user has the permission to access at least one endpoint
        """
        backend = JWTAuthentication()
        user = backend.authenticate(request)
        if user is not None:
            user, _ = user
            return user.is_active and user.is_staff
        return False

    def admin_view(self, view):
        def wrapper(request, *args, **kwargs):
            if self.has_permission(request):
                return view(request, *args, **kwargs)
            return HttpResponseForbidden(
                "You are not allowed to access this page",
                content_type="text/plain",
            )

        return wrapper

    def build_apps_dict(self, label=None):
        """
        Return a dictionary containing the apps and their models that it registered
        here. If some app doesn't have any model registered it will be ignored.
        The label might be used to filter the apps
        """
        if label:
            models = {
                model: model_admin
                for model, model_admin in self._registry.items()
                if model._meta.app_label == label
            }
        else:
            models = self._registry
        apps_dict = {}
        for model in models:
            app_label = model._meta.app_label
            model_name = capfirst(model._meta.verbose_name_plural)
            model_dict = {"model_name": model_name}
            if app_label in apps_dict:
                apps_dict[app_label]["models"].append(model_dict)
            else:
                apps_dict[app_label] = {"models": [model_dict]}
        return apps_dict

    def get_perms(self, request, model):
        pass

    @method_decorator(api_view())
    def index(self, request):
        return Response({"apps": self.build_apps_dict()})

    def get_urls(self):
        # avoid circuler imports
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_view(view)(*args, **kwargs)

            return wrapper

        urls = [path("", wrap(self.index), name="index")]
        return urls

    @property
    def urls(self):
        return self.get_urls(), "rest_admin", "rest_admin"


site = AdminSite()
