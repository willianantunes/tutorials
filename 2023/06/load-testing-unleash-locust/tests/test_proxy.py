import unittest

from dataclasses import dataclass

import wrapt

from requests.exceptions import MissingSchema
from UnleashClient import UnleashClient
from UnleashClient import register_client
from UnleashClient.api import get_feature_toggles
from UnleashClient.api import send_metrics


@dataclass(frozen=True)
class ErrorDetails:
    _type: str
    message: str
    exception: Exception | None = None


class TestProxy(unittest.TestCase):
    def test_patch_logger(self):
        error_holder = {}

        class CallableWrapper(wrapt.ObjectProxy):
            _self_unexpected_messages = ["fetch failed due to", "submission failed", "due to exception"]

            def __init__(self, wrapped: object, target: str):
                super().__init__(wrapped)
                self._self_target = target

            def _store_error_message_if_required(self, key_name: str, args: tuple):
                message = args[0].lower()
                if any([exception for exception in self._self_unexpected_messages if exception in message]):
                    array = error_holder.get(self._self_target, [])
                    if len(args) == 1:
                        array.append(ErrorDetails(key_name, message))
                        error_holder[self._self_target] = array
                    elif len(args) == 2:
                        raised_exception = args[1]
                        array.append(ErrorDetails(key_name, message, raised_exception))
                        error_holder[self._self_target] = array

            def warning(self, *args, **kwargs):
                self._store_error_message_if_required(self.warning.__name__, args)
                return self.__wrapped__.warning(*args, **kwargs)

            def exception(self, *args, **kwargs):
                self._store_error_message_if_required(self.exception.__name__, args)
                return self.__wrapped__.warning(*args, **kwargs)

        # Collect object
        unleash_client_api_features_module = __import__("UnleashClient").api.features
        unleash_client_api_features_logger = getattr(unleash_client_api_features_module, "LOGGER")
        unleash_client_api_metrics_module = __import__("UnleashClient").api.metrics
        unleash_client_api_metrics_logger = getattr(unleash_client_api_metrics_module, "LOGGER")
        unleash_client_api_register_module = __import__("UnleashClient").api.register
        unleash_client_api_register_logger = getattr(unleash_client_api_register_module, "LOGGER")
        # Set proxies
        api_features_proxy = CallableWrapper(unleash_client_api_features_logger, "api.features")
        setattr(unleash_client_api_features_module, "LOGGER", api_features_proxy)
        api_metrics_proxy = CallableWrapper(unleash_client_api_metrics_logger, "api.metrics")
        setattr(unleash_client_api_metrics_module, "LOGGER", api_metrics_proxy)
        api_register_proxy = CallableWrapper(unleash_client_api_register_logger, "api.register")
        setattr(unleash_client_api_register_module, "LOGGER", api_register_proxy)
        # Act
        send_metrics("fake-url", {}, {}, {})
        get_feature_toggles("fake-url", "", "", {}, {})
        with self.assertRaises(MissingSchema):
            register_client("fake-url", "", "", 1, {}, {}, {})
        # Assert
        expected = {
            "api.features": [
                ErrorDetails(
                    _type="exception",
                    message="unleash client feature fetch failed " "due to exception: %s",
                    exception=MissingSchema(
                        "Invalid URL 'fake-url/client/features': No scheme supplied. Perhaps you meant https://fake-url/client/features?"
                    ),
                )
            ],
            "api.metrics": [
                ErrorDetails(
                    _type="warning",
                    message="unleash client metrics submission " "failed due to exception: %s",
                    exception=MissingSchema(
                        "Invalid URL 'fake-url/client/metrics': No scheme supplied. Perhaps you meant https://fake-url/client/metrics?"
                    ),
                )
            ],
            "api.register": [
                ErrorDetails(
                    _type="exception",
                    message="unleash client registration failed " "fatally due to exception: %s",
                    exception=MissingSchema(
                        "Invalid URL 'fake-url/client/register': No scheme supplied. Perhaps you meant https://fake-url/client/register?"
                    ),
                )
            ],
        }
        self.assertEqual(expected, error_holder)

    def test_patch_fetch_and_load_features(self):
        # Arrange
        caller_holder = {}

        class CallableWrapper(wrapt.ObjectProxy):
            def __call__(self, *args, **kwargs):
                counter = caller_holder.get(self.__wrapped__.__name__, 0) + 1
                caller_holder[self.__wrapped__.__name__] = counter
                return self.__wrapped__(*args, **kwargs)

        unleash_client_module = __import__("UnleashClient")
        target_fetch_and_load_features = getattr(unleash_client_module, "fetch_and_load_features")
        setattr(unleash_client_module, "fetch_and_load_features", CallableWrapper(target_fetch_and_load_features))
        # Act
        UnleashClient("http://fake/api", "agrabah").initialize_client()
        # Assert
        self.assertTrue(caller_holder.get("fetch_and_load_features"))
        self.assertTrue(1, caller_holder["fetch_and_load_features"])
