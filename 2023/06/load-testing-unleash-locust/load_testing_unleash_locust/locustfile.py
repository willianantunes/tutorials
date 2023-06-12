import json
import logging
import time

import locust.env

from locust import between
from locust import events
from locust import task
from locust.runners import MasterRunner
from user_clients.unleash_client import BackendUser


@events.test_start.add_listener
def on_test_start(environment: locust.env.Environment, **kwargs):
    logging.info("Initiating the tests emulating a backend application...")


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        logging.info("I'm on master node")
    else:
        logging.info("I'm on a worker or standalone node")


class LoadTestBackEndClient(BackendUser):
    test_plan_key = "TEST_PLAN"
    wait_time = between(1, 5)

    def _check_toggle(self, key: str, call_is_enabled_if_true_or_variant_if_false: bool):
        method_to_be_called = "is_enabled" if call_is_enabled_if_true_or_variant_if_false else "get_variant"
        start_time = time.time()
        start_perf_counter = time.perf_counter()
        request_meta = {
            "request_type": method_to_be_called,
            "name": key,
            "context": {},
            "start_time": start_time,
            "response_length": 0,
        }
        response = None
        try:
            # Extracting expected value
            test_plan = self.unleash_client.get_variant(self.test_plan_key)
            toggles = json.loads(test_plan["payload"]["value"])
            expected_value = bool(toggles[key]) if call_is_enabled_if_true_or_variant_if_false else toggles[key]
            # Extracting actual value
            method_to_be_called_object = getattr(self.unleash_client, method_to_be_called)
            response = bool_or_variant = method_to_be_called_object(key)
            if not call_is_enabled_if_true_or_variant_if_false:
                actual_value = bool_or_variant["payload"]["value"]
                acceptable_variant = actual_value in expected_value
                assert acceptable_variant, f"{key} is {actual_value}, accepted values are {expected_value}"
            else:
                actual_value = bool_or_variant
                assert actual_value == expected_value, f"{key} is {actual_value}, the expected is {expected_value}"
        except Exception as e:
            request_meta["exception"] = e
        response_time = (time.perf_counter() - start_perf_counter) * 1000
        # This is what makes the request actually get logged in Locust!
        request_meta = request_meta | {"response_time": response_time, "response": response}
        self.environment.events.request.fire(**request_meta)

    @task
    def check_enable_profile_admin(self):
        key = "ENABLE_PROFILE_ADMIN"
        self._check_toggle(key, call_is_enabled_if_true_or_variant_if_false=True)

    @task
    def check_enable_profile_api(self):
        key = "ENABLE_PROFILE_API"
        self._check_toggle(key, call_is_enabled_if_true_or_variant_if_false=True)

    @task
    def check_show_profiles(self):
        key = "SHOW_PROFILES"
        self._check_toggle(key, call_is_enabled_if_true_or_variant_if_false=True)

    @task
    def check_allow_profile_management(self):
        key = "ALLOW_PROFILE_MANAGEMENT"
        self._check_toggle(key, call_is_enabled_if_true_or_variant_if_false=True)

    @task
    def check_variant_profile_management_button_scheme(self):
        key = "PROFILE_MANAGEMENT_BUTTON_SCHEME"
        self._check_toggle(key, call_is_enabled_if_true_or_variant_if_false=False)

    @task
    def check_show_easter_egg(self):
        key = "SHOW_EASTER_EGG"
        self._check_toggle(key, call_is_enabled_if_true_or_variant_if_false=True)
