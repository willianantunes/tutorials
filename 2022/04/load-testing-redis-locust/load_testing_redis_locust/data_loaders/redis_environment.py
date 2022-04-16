import logging

import redis

from common import settings
from django.core.cache.backends.redis import RedisSerializer


def _set_many(pipeline, data, timeout):
    pipeline.mset({k: RedisSerializer().dumps(v) for k, v in data.items()})
    for key in data:
        pipeline.expire(key, timeout)
    pipeline.execute()


def load_data_into_redis():
    redis_instance = redis.from_url(settings.REDIS_CONNECTION_STRING)
    base_key = settings.DATA_LOADER_REDIS_BASE_KEY
    number_of_keys = settings.DATA_LOADER_REDIS_ENTRIES_BY_KEY
    logging.info(f"Creating {number_of_keys*2} keys")
    sample_value_user_metadata = {
        "birthday": "1985-03-23",
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
    sample_value_m2m_tokens = {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL3NhbGFyLXV5dW5pLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJiYWNQeTU2bEhQamM0VHk2Z094aEpucFpBMlc1YlplWUBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9zYWxhci11eXVuaS51cy5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTY0NjQwMDQ0OCwiZXhwIjoxNjQ5OTc2NTEyLCJhenAiOiJiYWNQeTU2bEhQamM0VHk2Z094aEpucFpBMlc1YlplWSIsInNjb3BlIjoicmVhZDp1c2VycyB1cGRhdGU6dXNlcnMgZGVsZXRlOnVzZXJzIGNyZWF0ZTp1c2VycyByZWFkOnVzZXJzX2FwcF9tZXRhZGF0YSB1cGRhdGU6dXNlcnNfYXBwX21ldGFkYXRhIGRlbGV0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgY3JlYXRlOnVzZXJzX2FwcF9tZXRhZGF0YSByZWFkOnVzZXJfY3VzdG9tX2Jsb2NrcyBjcmVhdGU6dXNlcl9jdXN0b21fYmxvY2tzIGRlbGV0ZTp1c2VyX2N1c3RvbV9ibG9ja3MiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.lJ9saKPaZ-s4LWQrBYQJCakDrYOFpqLz_Of7dZySagP8bwUVeeCAHe0GEQMw9ND8IDTBOU5e2a_wO5sQIq5yger8xN37a5T3tlOCDP-W-qy4hmoJCw2cQkABGPG5F-ZXqGSVTi-P4zbby76LltVkKoRVqWnSj1Wg1JxTchfbGqlIY6yVOfUHFQps2ax3kee9JCZiif_uaQqQNajF02ZtyvTB-4XU4IqkovcMipM0QuBYdzPd7JbDsSkcbLyEhFfxH8Tn95uXjk1gmpNQn0i6LlRui40VXJ3c4dcGcg8fR8aUzpxjR6nIWoZ_VJFSOBO07NBrFmn9QNv4Q5YRr7sATg",
        "scope": "read:users update:users delete:users create:users read:users_app_metadata update:users_app_metadata delete:users_app_metadata create:users_app_metadata read:user_custom_blocks create:user_custom_blocks delete:user_custom_blocks",
        "expires_in": 86400,
        "token_type": "Bearer",
    }
    claims_dict_keys = {}
    m2m_tokens_dict_keys = {}
    for i in range(number_of_keys):
        claims_dict_keys[f"{base_key}_CLAIMS_{i}"] = sample_value_user_metadata
        m2m_tokens_dict_keys[f"{base_key}_M2M_{i}"] = sample_value_m2m_tokens
    logging.info("Cleaning current keys")
    claims_dict_keys.keys()
    redis_instance.delete(*[*claims_dict_keys])
    redis_instance.delete(*[*m2m_tokens_dict_keys])
    current_info = redis_instance.info()
    logging.info("Current value of used_memory_human: %s", current_info["used_memory_human"])
    logging.info("Current value of used_memory_peak_human: %s", current_info["used_memory_peak_human"])
    ten_minutes = 60 * 10
    # Doing the thing for `claims_dict_keys`
    logging.info("Pipeline with claims_dict_keys...")
    _set_many(redis_instance.pipeline(), claims_dict_keys, ten_minutes)
    # Doing the thing for `m2m_tokens_dict_keys`
    logging.info("Pipeline with m2m_tokens_dict_keys...")
    _set_many(redis_instance.pipeline(), m2m_tokens_dict_keys, ten_minutes)
    current_info = redis_instance.info()
    logging.info("Current value of used_memory_human: %s", current_info["used_memory_human"])
    logging.info("Current value of used_memory_peak_human: %s", current_info["used_memory_peak_human"])
