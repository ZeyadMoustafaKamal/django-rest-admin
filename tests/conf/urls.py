from django.urls import path

from rest_admin.site import site


urlpatterns = [
    path("admin/", site.urls)
]
