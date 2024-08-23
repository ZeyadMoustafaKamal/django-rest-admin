import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.conf.settings")
from django.core.management import execute_from_command_line # noqa: E402

execute_from_command_line()

