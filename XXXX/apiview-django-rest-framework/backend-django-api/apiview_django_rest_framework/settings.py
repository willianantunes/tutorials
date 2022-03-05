import os

from logging import Formatter
from pathlib import Path
from typing import Optional

from corsheaders.defaults import default_headers
from dotenv import load_dotenv

from apiview_django_rest_framework.apps.core.apps import CoreConfig
from apiview_django_rest_framework.support.django_helpers import eval_env_as_boolean
from apiview_django_rest_framework.support.django_helpers import getenv_or_raise_exception

BASE_DIR = Path(__file__).resolve().parent.parent

# TODO: Remove this
load_dotenv(BASE_DIR.joinpath(".env.development"), verbose=True)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-0&1_jbj^*owud8ls4hhtfz50@znj5$ntte_o@ny55w(ln$8_7&"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = eval_env_as_boolean("DJANGO_DEBUG", False)

DJANGO_ALLOWED_HOSTS: Optional[str] = os.getenv("ALLOWED_HOSTS")
if DJANGO_ALLOWED_HOSTS:
    EXTRA_ALLOWED_HOST: Optional[str] = os.getenv("EXTRA_ALLOWED_HOST")
    FINAL_ALLOWED_HOSTS = f"{DJANGO_ALLOWED_HOSTS},{EXTRA_ALLOWED_HOST}" if EXTRA_ALLOWED_HOST else DJANGO_ALLOWED_HOSTS
    ALLOWED_HOSTS = FINAL_ALLOWED_HOSTS.split(",")
else:
    ALLOWED_HOSTS = ["*"]

###############################
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_extensions",
    "apiview_django_rest_framework.apps.core",
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

###############################
# CORS

DISABLE_CORS = eval_env_as_boolean("DISABLE_CORS", False)
INSTALLED_APPS.append("corsheaders")
MIDDLEWARE.insert(1, "corsheaders.middleware.CorsMiddleware")
CORS_ALLOW_HEADERS = list(default_headers) + ["x-api-key"]

if not DISABLE_CORS:
    CORS_ALLOW_ALL_ORIGINS = eval_env_as_boolean("CORS_ALLOW_ALL_ORIGINS", False)
    CORS_ALLOW_CREDENTIALS = eval_env_as_boolean("CORS_ALLOW_CREDENTIALS", False)

    TMP_CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS")
    if TMP_CORS_ALLOWED_ORIGINS:
        if "," in TMP_CORS_ALLOWED_ORIGINS:
            CORS_ALLOWED_ORIGINS = [origin for origin in TMP_CORS_ALLOWED_ORIGINS.split(",")]
        else:
            CORS_ALLOWED_ORIGINS = [TMP_CORS_ALLOWED_ORIGINS]
    TMP_CORS_EXPOSE_HEADERS = os.getenv("CORS_EXPOSE_HEADERS")
    CORS_EXPOSE_HEADERS = TMP_CORS_EXPOSE_HEADERS.split(",") if TMP_CORS_EXPOSE_HEADERS else []
else:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True

###############################
# Continuation of the application definition

ROOT_URLCONF = "apiview_django_rest_framework.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "apiview_django_rest_framework.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.CursorPagination",
    "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 20)),
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (),
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Logging
# https://docs.djangoproject.com/en/4.0/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "()": Formatter,
            "format": "%(levelname)-8s [%(asctime)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": os.getenv("DEFAULT_LOG_FORMATTER", "standard"),
        }
    },
    "loggers": {
        "": {"level": os.getenv("ROOT_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "apiview_django_rest_framework": {
            "level": os.getenv("PROJECT_LOG_LEVEL", "INFO"),
            "handlers": ["console"],
            "propagate": False,
        },
        "django": {"level": os.getenv("DJANGO_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "django.db.backends": {"level": os.getenv("DJANGO_DB_BACKENDS_LOG_LEVEL", "INFO"), "handlers": ["console"]},
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

###############################
# Custom settings: Auth0

AUTH0_DOMAIN = getenv_or_raise_exception("AUTH0_DOMAIN")
AUTH0_TENANT_OPENID_CONFIGURATION = f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration"
AUTH0_TENANT_JWKS = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
AUTH0_MY_APPLICATION_AUDIENCE = getenv_or_raise_exception("AUTH0_MY_APPLICATION_AUDIENCE")
AUTH0_MY_APPLICATION_KEY = getenv_or_raise_exception("AUTH0_MY_APPLICATION_KEY")
AUTH0_MY_APPLICATION_SECRET = getenv_or_raise_exception("AUTH0_MY_APPLICATION_SECRET")
