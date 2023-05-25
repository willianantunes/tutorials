import os

from common.support import getenv_or_raise_exception

UNLEASH_API_ADMIN_TOKEN = getenv_or_raise_exception("UNLEASH_API_ADMIN_TOKEN")
UNLEASH_APP_NAME_PREFIX = os.getenv("UNLEASH_APP_NAME_PREFIX", "app-backend")
UNLEASH_URL = os.getenv("UNLEASH_URL", "http://unleash:4242")
