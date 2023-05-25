import logging
import time

from dataclasses import dataclass
from uuid import uuid4

import locust.env
import wrapt

from common import settings
from common.feature_management import AdminUnleash
from common.feature_management import ClientUnleash
from UnleashClient import UnleashClient

# These are the original functions
unleash_client_module = __import__("UnleashClient")
target_load_features = getattr(unleash_client_module, "load_features")
fetch_and_load_features = getattr(unleash_client_module, "fetch_and_load_features")
aggregate_and_send_metrics = getattr(unleash_client_module, "aggregate_and_send_metrics")
register_client = getattr(unleash_client_module, "register_client")
# The exception is not raised, it's caught and logged, so we should patch this also
unleash_client_api_features_module = __import__("UnleashClient").api.features
unleash_client_api_features_logger = getattr(unleash_client_api_features_module, "LOGGER")
unleash_client_api_metrics_module = __import__("UnleashClient").api.metrics
unleash_client_api_metrics_logger = getattr(unleash_client_api_metrics_module, "LOGGER")
unleash_client_api_register_module = __import__("UnleashClient").api.register
unleash_client_api_register_logger = getattr(unleash_client_api_register_module, "LOGGER")


@dataclass(frozen=True)
class ErrorDetails:
    _type: str
    message: str
    exception: Exception | None = None


class UnleashClientWrapped(wrapt.ObjectProxy):
    def __init__(self, wrapped, locust_handler):
        super(UnleashClientWrapped, self).__init__(wrapped)
        self._self_wrapper = locust_handler

    def is_enabled(self, *args, **kwargs):
        return self._self_wrapper(self.__wrapped__.is_enabled, args, kwargs)

    def get_variant(self, *args, **kwargs):
        return self._self_wrapper(self.__wrapped__.get_variant, args, kwargs)


class BackendUser(locust.User):
    abstract = True
    unleash_client: UnleashClient

    def __init__(self, environment):
        super().__init__(environment)
        self.error_holder = {}

    def on_start(self):
        # This is used inside locust_handler method
        request_event = self.environment.events.request

        self.error_holder = {}
        logging.info("Changing load features")

        class CallableLoggerWrapper(wrapt.ObjectProxy):
            _self_unexpected_messages = ["fetch failed due to", "submission failed", "due to exception"]

            def __init__(self, wrapped: object, target: str, error_holder: dict):
                super().__init__(wrapped)
                self._self_target = target
                self._self_error_holder = error_holder

            def _store_error_message_if_required(self, key_name: str, args: tuple):
                message = args[0].lower()
                if any([exception for exception in self._self_unexpected_messages if exception in message]):
                    array = self._self_error_holder.get(self._self_target, [])
                    if len(args) == 1:
                        array.append(ErrorDetails(key_name, message))
                        self._self_error_holder[self._self_target] = array
                    elif len(args) == 2:
                        raised_exception = args[1]
                        array.append(ErrorDetails(key_name, message, raised_exception))
                        self._self_error_holder[self._self_target] = array

            def warning(self, *args, **kwargs):
                self._store_error_message_if_required(self.warning.__name__, args)
                return self.__wrapped__.warning(*args, **kwargs)

            def exception(self, *args, **kwargs):
                self._store_error_message_if_required(self.exception.__name__, args)
                return self.__wrapped__.warning(*args, **kwargs)

        class CallableWrapper(wrapt.ObjectProxy):
            def __init__(self, wrapped: object, key_name: str = None, error_holder: dict = None):
                super().__init__(wrapped)
                self._self_key_name = key_name
                self._self_error_holder = error_holder

            def __call__(self, *args, **kwargs):
                # Do something before the load_features function is called
                start_time = time.time()
                start_perf_counter = time.perf_counter()
                request_meta = {
                    "request_type": "Unleash Scheduler",
                    "name": self.__wrapped__.__name__,
                    "context": {},
                    "start_time": start_time,
                    "response_length": 0,
                }
                result = None
                try:
                    result = self.__wrapped__(*args, **kwargs)
                except Exception as e:
                    request_meta["exception"] = e
                if request_meta.get("exception") is None and self._self_key_name:
                    must_inform_exception = self._self_key_name in self._self_error_holder
                    if must_inform_exception:
                        # It's not totally guaranteed the error matches the one raised by this user
                        # Each user has a ThreadPoolExecutor, so while this code executes, another error could be raised
                        # Check `CallableLoggerWrapper` to understand the logic behind the curtains
                        errors = self._self_error_holder[self._self_key_name]
                        latest_error: ErrorDetails = errors.pop()
                        request_meta["exception"] = latest_error
                        errors.clear()
                        self._self_error_holder[self._self_key_name] = errors
                response_time = (time.perf_counter() - start_perf_counter) * 1000
                # This is what makes the request actually get logged in Locust!
                request_meta = request_meta | {"response_time": response_time, "response": result}
                request_event.fire(**request_meta)
                return result

        # Override the original functions each time a new user is instantiated
        # Each UnleashClient instance will have a dedicated `self.environment.events.request` to properly set metrics
        setattr(unleash_client_module, "load_features", CallableWrapper(target_load_features, None))
        fetch_and_load_features_proxy = CallableWrapper(fetch_and_load_features, "api.features", self.error_holder)
        setattr(unleash_client_module, "fetch_and_load_features", fetch_and_load_features_proxy)
        aggregate_and_send_metrics_proxy = CallableWrapper(aggregate_and_send_metrics, "api.metrics", self.error_holder)
        setattr(unleash_client_module, "aggregate_and_send_metrics", aggregate_and_send_metrics_proxy)
        register_client_proxy = CallableWrapper(register_client, "api.register", self.error_holder)
        setattr(unleash_client_module, "register_client", register_client_proxy)
        # To know when an error occurs
        features_logger = CallableLoggerWrapper(unleash_client_api_features_logger, "api.features", self.error_holder)
        setattr(unleash_client_api_features_module, "LOGGER", features_logger)
        metrics_logger = CallableLoggerWrapper(unleash_client_api_metrics_logger, "api.metrics", self.error_holder)
        setattr(unleash_client_api_metrics_module, "LOGGER", metrics_logger)
        register_logger = CallableLoggerWrapper(unleash_client_api_register_logger, "api.register", self.error_holder)
        setattr(unleash_client_api_register_module, "LOGGER", register_logger)

        logging.info("Configuring user...")
        admin_client = AdminUnleash(settings.UNLEASH_URL, settings.UNLEASH_API_ADMIN_TOKEN)
        app_name = f"{settings.UNLEASH_APP_NAME_PREFIX}-{uuid4()}"
        user_details = admin_client.create_api_token(app_name)
        user_secret = user_details["secret"]

        def locust_handler(wrapped, args, kwargs):
            feature_toggle_name = args[0]
            start_time = time.time()
            start_perf_counter = time.perf_counter()
            request_meta = {
                "request_type": wrapped.__name__,
                "name": feature_toggle_name,
                "context": {},
                "start_time": start_time,
                "response_length": 0,
            }
            try:
                response = wrapped(*args, **kwargs)
            except Exception as e:
                request_meta["exception"] = e
            response_time = (time.perf_counter() - start_perf_counter) * 1000
            # This is what makes the request actually get logged in Locust!
            request_meta = request_meta | {"response_time": response_time, "response": response}
            request_event.fire(**request_meta)
            return response

        self._unleash_client = ClientUnleash(f"{settings.UNLEASH_URL}/api", user_secret, app_name).connect()
        self.unleash_client = UnleashClientWrapped(self._unleash_client, locust_handler)
        logging.info("User has been configured")

    def on_stop(self):
        self._unleash_client.destroy()
