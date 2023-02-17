import os

import environ

from tests.interfaces import Addition, Division, NormCalculation, Power

env = environ.Env(
    DB_NAME=(str, "django_analyses"),
    DB_USER=(str, ""),
    DB_PASSWORD=(str, ""),
    DB_HOST=(str, "localhost"),
    DB_PORT=(int, 5432),
)
environ.Env.read_env()

DEBUG = False
ALLOWED_HOSTS = ["localhost"]
SECRET_KEY = "sa8!1ep_9#36qw@i-3j(a4uikiobleh03jl8v_3!n^^dsm9oyc"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_AUTO_FIELD="django.db.models.AutoField"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "django_celery_results",
    "django_analyses",
    "tests",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ]
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = (os.path.join(BASE_DIR, "static"),)

MEDIA_ROOT = os.path.join(BASE_DIR, "tests")
MEDIA_URL = "/media/"
ROOT_URLCONF = "django_analyses.urls"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

ANALYSIS_BASE_PATH = os.path.join(BASE_DIR, "media", "analysis")

ANALYSIS_INTERFACES = {
    "addition": {"1.0": Addition},
    "division": {"1.0": Division},
    "norm": {"NumPy:1.18": NormCalculation},
    "power": {"1.0": Power},
}

# Date format
DATE_FORMAT = "d/m/Y"

# Time format
TIME_FORMAT = "H:i:s"

# Datetime format
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

# Time zone
USE_TZ = True
TIME_ZONE = "Asia/Jerusalem"