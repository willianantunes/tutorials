import logging

import locust.env

from locust import User
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
    wait_time = between(1, 5)

    @task
    def check_enable_profile_admin(self):
        self.unleash_client.is_enabled("ENABLE_PROFILE_ADMIN")

    @task
    def check_enable_profile_api(self):
        self.unleash_client.is_enabled("ENABLE_PROFILE_API")

    @task
    def check_show_profiles(self):
        self.unleash_client.is_enabled("SHOW_PROFILES")

    @task
    def check_allow_profile_management(self):
        self.unleash_client.is_enabled("ALLOW_PROFILE_MANAGEMENT")

    @task
    def check_your_are_special_for_us(self):
        self.unleash_client.is_enabled("YOU_ARE_SPECIAL_FOR_US")

    @task
    def check_variant_profile_management_button_scheme(self):
        self.unleash_client.get_variant("PROFILE_MANAGEMENT_BUTTON_SCHEME")

    @task
    def check_variant_text_presentation(self):
        self.unleash_client.get_variant("TEXT_PRESENTATION")

    @task
    def check_game_shark_mode(self):
        self.unleash_client.is_enabled("GAME_SHARK_MODE")

    @task
    def check_add_post(self):
        self.unleash_client.is_enabled("ADD_POST")

    @task
    def check_disable_claims_page(self):
        self.unleash_client.is_enabled("DISABLE_CLAIMS_PAGE")

    @task
    def check_show_easter_egg(self):
        self.unleash_client.is_enabled("SHOW_EASTER_EGG")

    @task
    def check_show_tags(self):
        self.unleash_client.is_enabled("SHOW_TAGS")

    @task
    def check_variant_button_scheme_value(self):
        self.unleash_client.get_variant("BUTTON_SCHEME_VALUE")
