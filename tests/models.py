from django.db import models


class Model(models.Model):
    "Base class For all testing models"

    class Meta:
        app_label = "tests"
        abstract = True
