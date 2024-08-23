DEUBG = True

ROOT_URLCONF = "tests.conf.urls"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    
    # local
    "tests",
    "rest_admin",
    
    # third party
    "rest_framework",
    "rest_framework_simplejwt",
]

SECRET_KEY = "a very secret key"


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "PATH": "db.sqlite3"}
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}
