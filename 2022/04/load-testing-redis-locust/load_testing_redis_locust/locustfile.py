import logging

from common import settings
from locust import events
from locust import task

from load_testing_redis_locust.data_loaders.redis_environment import load_data_into_redis
from load_testing_redis_locust.user_clients.django_redis_client import DjangoRedisUser


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logging.info("Loading data into Redis!")
    load_data_into_redis()


class PerformanceTest(DjangoRedisUser):
    base_key = settings.DATA_LOADER_REDIS_BASE_KEY
    entries = settings.DATA_LOADER_REDIS_ENTRIES_BY_KEY

    @task
    def save_value_to_key_with_5sec_timeout_claim_1(self):
        key = f"{self.base_key}_CLAIMS_1"
        value = {
            "gender": "female",
            "addresses": [
                {
                    "identification": "billing",
                    "country": "BR",
                    "stateOrProvince": "GO",
                    "city": "Inhumas",
                    "houseNumberOrName": "42",
                    "street": "R Saleiro",
                    "postalCode": "75400000",
                },
                {
                    "identification": "home",
                    "country": "BR",
                    "stateOrProvince": "BA",
                    "city": "Jequiezinho",
                    "houseNumberOrName": "16",
                    "street": "R do Sal",
                    "postalCode": "45204550",
                },
            ],
        }
        self.client.set(key, value, timeout=5)

    @task
    def save_value_to_key_with_2sec_timeout_claim_2(self):
        key = f"{self.base_key}_CLAIMS_2"
        value = {
            "gender": "female",
            "addresses": [
                {
                    "identification": "billing",
                    "country": "BR",
                    "stateOrProvince": "GO",
                    "city": "Inhumas",
                    "houseNumberOrName": "42",
                    "street": "R Saleiro",
                    "postalCode": "75400000",
                },
                {
                    "identification": "home",
                    "country": "BR",
                    "stateOrProvince": "BA",
                    "city": "Jequiezinho",
                    "houseNumberOrName": "16",
                    "street": "R do Sal",
                    "postalCode": "45204550",
                },
                {
                    "identification": "billing",
                    "country": "BR",
                    "stateOrProvince": "GO",
                    "city": "Inhumas",
                    "houseNumberOrName": "42",
                    "street": "R Saleiro",
                    "postalCode": "75400000",
                },
                {
                    "identification": "home",
                    "country": "BR",
                    "stateOrProvince": "BA",
                    "city": "Jequiezinho",
                    "houseNumberOrName": "16",
                    "street": "R do Sal",
                    "postalCode": "45204550",
                },
                {
                    "identification": "billing",
                    "country": "BR",
                    "stateOrProvince": "GO",
                    "city": "Inhumas",
                    "houseNumberOrName": "42",
                    "street": "R Saleiro",
                    "postalCode": "75400000",
                },
                {
                    "identification": "home",
                    "country": "BR",
                    "stateOrProvince": "BA",
                    "city": "Jequiezinho",
                    "houseNumberOrName": "16",
                    "street": "R do Sal",
                    "postalCode": "45204550",
                },
            ],
        }
        self.client.set(key, value, timeout=2)

    @task
    def save_value_to_key_with_10sec_timeout_claim_3(self):
        key = f"{self.base_key}_CLAIMS_3"
        value = {
            "gender": "male",
            "addresses": [
                {
                    "identification": "billing",
                    "country": "BR",
                    "stateOrProvince": "GO",
                    "city": "Inhumas",
                    "houseNumberOrName": "42",
                    "street": "R Saleiro",
                    "postalCode": "75400000",
                },
                {
                    "identification": "home",
                    "country": "BR",
                    "stateOrProvince": "BA",
                    "city": "Jequiezinho",
                    "houseNumberOrName": "16",
                    "street": "R do Sal",
                    "postalCode": "45204550",
                },
                {
                    "identification": "billing",
                    "country": "BR",
                    "stateOrProvince": "GO",
                    "city": "Inhumas",
                    "houseNumberOrName": "42",
                    "street": "R Saleiro",
                    "postalCode": "75400000",
                },
                {
                    "identification": "home",
                    "country": "BR",
                    "stateOrProvince": "BA",
                    "city": "Jequiezinho",
                    "houseNumberOrName": "16",
                    "street": "R do Sal",
                    "postalCode": "45204550",
                },
                {
                    "identification": "billing",
                    "country": "BR",
                    "stateOrProvince": "GO",
                    "city": "Inhumas",
                    "houseNumberOrName": "42",
                    "street": "R Saleiro",
                    "postalCode": "75400000",
                },
                {
                    "identification": "home",
                    "country": "BR",
                    "stateOrProvince": "BA",
                    "city": "Jequiezinho",
                    "houseNumberOrName": "16",
                    "street": "R do Sal",
                    "postalCode": "45204550",
                },
                {
                    "identification": "billing",
                    "country": "BR",
                    "stateOrProvince": "GO",
                    "city": "Inhumas",
                    "houseNumberOrName": "42",
                    "street": "R Saleiro",
                    "postalCode": "75400000",
                },
                {
                    "identification": "home",
                    "country": "BR",
                    "stateOrProvince": "BA",
                    "city": "Jequiezinho",
                    "houseNumberOrName": "16",
                    "street": "R do Sal",
                    "postalCode": "45204550",
                },
            ],
        }
        self.client.set(key, value, timeout=10)

    @task
    def get_value_key_claim_1(self):
        key = f"{self.base_key}_CLAIMS_1"
        self.client.get(key)

    @task
    def get_value_key_claim_2(self):
        key = f"{self.base_key}_CLAIMS_2"
        self.client.get(key)

    @task
    def get_value_key_claim_3(self):
        key = f"{self.base_key}_CLAIMS_3"
        self.client.get(key)

    @task
    def retrieve_all_keys_from_claims_with_get_many(self):
        all_claims_keys = [f"{self.base_key}_CLAIMS_{index}" for index in range(self.entries)]
        self.client.get_many(all_claims_keys)

    @task
    def retrieve_all_keys_from_m2m_with_get_many(self):
        all_m2m_keys = [f"{self.base_key}_M2M_{index}" for index in range(self.entries)]
        self.client.get_many(all_m2m_keys)
