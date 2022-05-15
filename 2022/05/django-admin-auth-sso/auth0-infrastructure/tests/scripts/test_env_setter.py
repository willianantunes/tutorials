import json
import re
import unittest
import uuid

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

from scripts.env_setter import _load_content_as_string
from scripts.env_setter import _yielding_all_matching_files_from_directory
from tests.utils import create_files_with_content


class TestEnvSetter(unittest.TestCase):
    def test_should_list_all_files_from_directory(self):
        # Arrange
        tmp_folder = f"./tmp-tests-{uuid.uuid4()}"
        sample_files_with_content = [
            (f"jafar-{uuid.uuid4()}.env", "KEY=VALUE"),
            (f"agrabah-{uuid.uuid4()}.env", "KEY=VALUE"),
            (f"aladdin-{uuid.uuid4()}.txt", "The greatest show ever made!"),
        ]
        with create_files_with_content(sample_files_with_content, tmp_folder):
            glob_pattern = "*.env"
            # Act
            files = _yielding_all_matching_files_from_directory(tmp_folder, glob_pattern)
            # Assert
            number_of_files = len(files)
            self.assertEqual(2, number_of_files)

    def test_should_read_file_and_convert_content_to_dict(self):
        # Arrange
        content = """
            {
              "is_token_endpoint_ip_header_trusted": false,
              "name": "Product XYZ",
              "cross_origin_auth": false,
              "callbacks": @@PRODUCT_XYZ_URI@@,
              "allowed_logout_urls": @@PRODUCT_XYZ_URI@@,
              "is_first_party": true,
              "sso_disabled": false,
              "oidc_conformant": true,
              "refresh_token": {
                "expiration_type": "non-expiring",
                "leeway": 0,
                "infinite_token_lifetime": true,
                "infinite_idle_token_lifetime": true,
                "token_lifetime": 2592000,
                "idle_token_lifetime": 1296000,
                "rotation_type": "non-rotating"
              },
              "allowed_origins": @@PRODUCT_XYZ_URI@@,
              "jwt_configuration": {
                "alg": "RS256",
                "lifetime_in_seconds": 36000,
                "secret_encoded": false
              },
              "token_endpoint_auth_method": "none",
              "app_type": "spa",
              "grant_types": [
                "authorization_code",
                "implicit",
                "refresh_token"
              ],
              "web_origins": @@PRODUCT_XYZ_URI@@,
              "custom_login_page_on": true
            }       
        """
        sample_files_with_content = [
            (f"jafar-{uuid.uuid4()}.json", content),
        ]
        with create_files_with_content(sample_files_with_content) as created_files:
            self.assertEqual(1, len(created_files))
            jafar_file = created_files[0]
            # Act
            content = _load_content_as_string(jafar_file).replace("\n", "")
            content_after = re.sub(r"@@.+?@@", '""', content)
            content_as_dict = json.loads(content_after)
            # Assert
            expected_value = {
                "is_token_endpoint_ip_header_trusted": False,
                "name": "Product XYZ",
                "cross_origin_auth": False,
                "callbacks": "",
                "allowed_logout_urls": "",
                "is_first_party": True,
                "sso_disabled": False,
                "oidc_conformant": True,
                "refresh_token": {
                    "expiration_type": "non-expiring",
                    "leeway": 0,
                    "infinite_token_lifetime": True,
                    "infinite_idle_token_lifetime": True,
                    "token_lifetime": 2592000,
                    "idle_token_lifetime": 1296000,
                    "rotation_type": "non-rotating",
                },
                "allowed_origins": "",
                "jwt_configuration": {"alg": "RS256", "lifetime_in_seconds": 36000, "secret_encoded": False},
                "token_endpoint_auth_method": "none",
                "app_type": "spa",
                "grant_types": ["authorization_code", "implicit", "refresh_token"],
                "web_origins": "",
                "custom_login_page_on": True,
            }
            self.assertEqual(expected_value, content_as_dict)


@unittest.skip
class TestAuth0(unittest.TestCase):
    def test_should_retrieve_action_and_configure_secrets(self):
        # Arrange
        AUTH0_CLIENT_ID = "AUTH0_CLIENT_ID"
        AUTH0_CLIENT_SECRET = "AUTH0_CLIENT_SECRET"
        AUTH0_DOMAIN = "AUTH0_DOMAIN"
        get_token = GetToken(AUTH0_DOMAIN)
        auth0_endpoint = f"https://{AUTH0_DOMAIN}/api/v2/"
        token = get_token.client_credentials(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, auth0_endpoint)
        auth0 = Auth0(AUTH0_DOMAIN, token["access_token"])
        action_name = "Enrich JWT with Groups from AD"
        # Act
        actions_pagination = auth0.actions.get_actions(deployed=True, trigger_id="post-login", action_name=action_name)
        action = actions_pagination["actions"][0]
        action_id = action["id"]
        assert action_id
