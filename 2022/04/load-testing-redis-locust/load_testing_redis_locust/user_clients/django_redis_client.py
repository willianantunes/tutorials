import logging
import time

import django
import wrapt

from common import settings as app_settings
from django.conf import settings
from locust import User
from locust.env import Environment


class DjangoRedisClient(wrapt.ObjectProxy):
    def __init__(self, wrapped, locust_handler):
        super(DjangoRedisClient, self).__init__(wrapped)
        self._self_wrapper = locust_handler

    def get(self, *args, **kwargs):
        return self._self_wrapper(self.__wrapped__.get, args, kwargs)

    def get_many(self, *args, **kwargs):
        return self._self_wrapper(self.__wrapped__.get_many, args, kwargs)

    def set(self, *args, **kwargs):
        return self._self_wrapper(self.__wrapped__.set, args, kwargs)


class DjangoRedisUser(User):
    abstract = True

    def __init__(self, environment: Environment):
        super().__init__(environment)
        logging.info("Initializing user...")

        # Configure Django
        try:
            settings.configure(
                CACHES={
                    "default": {
                        "BACKEND": "django.core.cache.backends.redis.RedisCache",
                        "LOCATION": app_settings.REDIS_CONNECTION_STRING,
                    }
                }
            )
            django.setup()
        except RuntimeError as e:
            ignore_error = "already configured" in str(e).lower()
            if not ignore_error:
                raise e

        request_event = environment.events.request

        def locust_handler(wrapped, args, kwargs):
            custom_name = kwargs.get("name")
            request_meta = {
                "request_type": "Django’s cache framework (Redis)",
                "name": custom_name if custom_name else wrapped.__name__,
                "start_time": time.time(),
                "response_length": 0,
                "response": None,
                "context": {},
                "exception": None,
            }
            start_perf_counter = time.perf_counter()
            try:
                request_meta["response"] = wrapped(*args, **kwargs)
            except Exception as e:
                request_meta["exception"] = e
            request_meta["response_time"] = (time.perf_counter() - start_perf_counter) * 1000
            # This is what makes the request actually get logged in Locust!
            request_event.fire(**request_meta)
            return request_meta["response"]

        from django.core.cache import cache as original_cache

        self.client = DjangoRedisClient(original_cache, locust_handler)
