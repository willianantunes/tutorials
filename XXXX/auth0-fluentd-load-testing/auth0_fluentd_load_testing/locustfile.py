import json

from datetime import datetime
from random import randrange
from uuid import uuid4

from locust import HttpUser
from locust import between
from locust import run_single_user
from locust import task

try:
    from pathlib import Path

    from dotenv import load_dotenv

    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(BASE_DIR.joinpath(".env"), verbose=True)
except ImportError:
    pass

from auth0_fluentd_load_testing.common import settings


class Auth0Tenant(HttpUser):
    host = settings.API_GATEWAY_ENDPOINT
    wait_time = between(0.1, 0.5)

    def _post_to_fluentd(self, sample_entry):
        body = self._generate_sample_body(sample_entry)
        headers = {
            "Authorization": settings.FLUENT_AUTHORIZATION_TOKEN,
            "Content-Type": "application/json",
        }
        data = json.dumps(body)
        self.client.post(settings.FLUENTD_REQUEST_PATH, data=data, headers=headers)

    def _generate_sample_body(self, sample_entry):
        body = []
        number_of_entries = randrange(10, 101, 2)
        for _ in range(number_of_entries):
            sample_log_id = str(uuid4())
            sample_entry["date"] = datetime.utcnow().isoformat()
            entry = {
                "log_id": sample_log_id,
                "data": sample_entry,
            }
            body.append(entry)

        return body

    @task
    def informing_sapi_success_api_operation(self):
        body = {
            "type": "sapi",
            "description": "TESTING_PURPOSE",
            "client_id": "0K4d0DgZthpVjPgZ2T9lLvqMSqweveLt",
            "client_name": "",
            "ip": "52.255.188.22",
            "user_agent": "deploy-cli/7.12.1 (node.js/16.15.0)",
            "details": {
                "request": {
                    "method": "patch",
                    "path": "/api/v2/tenants/settings",
                    "query": {},
                    "userAgent": "deploy-cli/7.12.1 (node.js/16.15.0)",
                    "body": {
                        "enabled_locales": ["pt-BR"],
                        "flags": {
                            "universal_login": True,
                            "revoke_refresh_token_grant": False,
                            "disable_clickjack_protection_headers": False,
                        },
                        "friendly_name": "antunes DEV",
                        "picture_url": "https://assets-img.willianantunes.com/images/logo.svg",
                        "support_email": "atendimento@willianantunes.com",
                        "support_url": "https://github.com/willianantunes",
                    },
                    "channel": "api",
                    "ip": "52.255.188.22",
                    "auth": {
                        "user": {},
                        "strategy": "jwt",
                        "credentials": {
                            "scopes": [
                                "read:client_grants",
                                "create:client_grants",
                                "delete:client_grants",
                                "update:client_grants",
                                "read:clients",
                                "update:clients",
                                "delete:clients",
                                "create:clients",
                                "read:client_keys",
                                "update:client_keys",
                                "delete:client_keys",
                                "create:client_keys",
                                "read:connections",
                                "update:connections",
                                "delete:connections",
                                "create:connections",
                                "read:resource_servers",
                                "update:resource_servers",
                                "delete:resource_servers",
                                "create:resource_servers",
                                "read:rules",
                                "update:rules",
                                "delete:rules",
                                "create:rules",
                                "read:rules_configs",
                                "update:rules_configs",
                                "delete:rules_configs",
                                "read:hooks",
                                "update:hooks",
                                "delete:hooks",
                                "create:hooks",
                                "read:actions",
                                "update:actions",
                                "delete:actions",
                                "create:actions",
                                "read:email_provider",
                                "update:email_provider",
                                "delete:email_provider",
                                "create:email_provider",
                                "read:tenant_settings",
                                "update:tenant_settings",
                                "read:grants",
                                "delete:grants",
                                "read:guardian_factors",
                                "update:guardian_factors",
                                "read:email_templates",
                                "create:email_templates",
                                "update:email_templates",
                                "read:mfa_policies",
                                "update:mfa_policies",
                                "read:roles",
                                "create:roles",
                                "delete:roles",
                                "update:roles",
                                "read:prompts",
                                "update:prompts",
                                "read:branding",
                                "update:branding",
                                "read:attack_protection",
                                "update:attack_protection",
                                "read:organizations",
                                "update:organizations",
                                "create:organizations",
                                "delete:organizations",
                                "create:organization_connections",
                                "read:organization_connections",
                                "update:organization_connections",
                                "delete:organization_connections",
                            ]
                        },
                    },
                },
                "response": {
                    "statusCode": 200,
                    "body": {
                        "default_audience": "",
                        "default_directory": "Username-Password-Authentication",
                        "enabled_locales": ["pt-BR"],
                        "flags": {
                            "allow_changing_enable_sso": False,
                            "cannot_change_enforce_client_authentication_on_passwordless_start": True,
                            "disable_impersonation": True,
                            "enable_sso": True,
                            "enforce_client_authentication_on_passwordless_start": True,
                            "universal_login": True,
                            "revoke_refresh_token_grant": False,
                            "disable_clickjack_protection_headers": False,
                        },
                        "friendly_name": "antunes DEV",
                        "picture_url": "https://assets-img.willianantunes.com/images/logo.svg",
                        "sandbox_version": "12",
                        "support_email": "atendimento@willianantunes.com",
                        "support_url": "https://github.com/willianantunes",
                    },
                },
            },
            "auth0_client": {"name": "node-auth0", "version": "2.40.0", "env": {"node": "16.15.0"}},
            "log_id": "90020220511211012650264478360083282282262616966841761810",
        }
        self._post_to_fluentd(body)

    @task
    def informing_feacft_failed_exchange(self):
        body = {
            "type": "feacft",
            "description": "TESTING_PURPOSE",
            "connection_id": "",
            "client_id": "UegcnFxLgYbJSVwQEv82cgv9B4Bq6poZ",
            "client_name": "All Applications",
            "ip": "35.166.202.113",
            "user_agent": "Node-oauth",
            "details": {"code": "******************************************YaA"},
            "hostname": "testing.us.auth0.com",
            "user_id": "",
            "user_name": "",
            "log_id": "90020220512180414981927509633181027507848496495863005186",
        }
        self._post_to_fluentd(body)

    @task
    def informing_ss_success_signup(self):
        body = {
            "type": "ss",
            "description": "TESTING_PURPOSE",
            "connection": "Username-Password-Authentication",
            "connection_id": "con_dKkvABJlA29FWlKd",
            "client_id": "Rx1g3skPruIbVKqYgFVa3SO9QiOKsAbm",
            "client_name": "Temporary My App",
            "ip": "3.220.150.63",
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
            "details": {
                "body": {
                    "connection": "Username-Password-Authentication",
                    "client_id": "Rx1g3skPruIbVKqYgFVa3SO9QiOKsAbm",
                    "email": "willia.n.lima.antunes@gmail.com",
                    "password": "*****",
                    "tenant": "antunes",
                    "transaction": {
                        "id": "lmiJmerKiNWXvF9ovK6IPTk5QW0l4c3P",
                        "locale": "pt-BR",
                        "protocol": "oidc-basic-profile",
                        "requested_scopes": ["openid", "profile", "email"],
                        "acr_values": [],
                        "ui_locales": [],
                        "redirect_uri": "http://app.local:8000/api/v1/response-oidc",
                        "prompt": [],
                        "state": "965fbb58-a37d-4268-8e14-3baf7971a62b",
                        "login_hint": None,
                        "response_mode": None,
                        "response_type": ["code"],
                    },
                    "request_language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
                }
            },
            "user_id": "auth0|624d97dd754ef9006f7a3785",
            "user_name": "willia.n.lima.antunes@gmail.com",
            "strategy": "auth0",
            "strategy_type": "database",
            "log_id": "90020220406133840374262863680862407315867429212948267026",
        }
        self._post_to_fluentd(body)

    @task
    def informing_s_success_login(self):
        body = {
            "type": "s",
            "connection_id": "",
            "client_id": "TESTING_PURPOSE",
            "client_name": "TESTING_PURPOSE",
            "ip": "3.220.150.63",
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
            "details": {
                "prompts": [
                    {
                        "name": "prompt-signup",
                        "completedAt": 1649252317345,
                        "connection": "Username-Password-Authentication",
                        "connection_id": "con_dKkvABJlA29FWlKd",
                        "strategy": "auth0",
                        "identity": "624d97dd754ef9006f7a3785",
                        "stats": {"loginsCount": 1},
                        "elapsedTime": None,
                    },
                    {
                        "name": "login",
                        "flow": "universal-login",
                        "initiatedAt": 1649252284229,
                        "completedAt": 1649252317400,
                        "timers": {"rules": 11},
                        "user_id": "auth0|624d97dd754ef9006f7a3785",
                        "user_name": "willia.n.lima.antunes@gmail.com",
                        "elapsedTime": 33171,
                    },
                ],
                "initiatedAt": 1649252284214,
                "completedAt": 1649252317784,
                "elapsedTime": 33570,
                "session_id": "crk4ShpUyZC-cAURvl-pNWQU1QuWJK_5",
            },
            "hostname": "agrabah-antunes-dev.us.auth0.com",
            "user_id": "auth0|624d97dd754ef9006f7a3785",
            "user_name": "willia.n.lima.antunes@gmail.com",
            "log_id": "90020220406133842652921656700924724616333398529087111170",
        }
        self._post_to_fluentd(body)

    @task
    def informing_flo_failed_logout(self):
        body = {
            "type": "flo",
            "description": "TESTING_PURPOSE",
            "connection": "Username-Password-Authentication",
            "connection_id": "con_dKkvABJlA29FWlKd",
            "client_id": "Rx1g3skPruIbVKqYgFVa3SO9QiOKsAbm",
            "client_name": "Temporary My App",
            "ip": "3.220.150.63",
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
            "details": {
                "return_to": "http://app.local:8000/logout",
                "allowed_logout_url": ["http://app.local:8000/"],
                "session_id": "crk4ShpUyZC-cAURvl-pNWQU1QuWJK_5",
            },
            "hostname": "agrabah-antunes-dev.us.auth0.com",
            "user_id": "auth0|624d97dd754ef9006f7a3785",
            "user_name": "willia.n.lima.antunes@gmail.com",
            "log_id": "90020220406133846342262863684034628666536216579694133266",
        }
        self._post_to_fluentd(body)

    @task
    def informing_gd_tenant_update_guardian_tenant_update(self):
        body = {
            "type": "gd_tenant_update",
            "description": "TESTING_PURPOSE",
            "ip": "52.255.188.22",
            "details": {
                "request": {
                    "method": "PATCH",
                    "path": "/api/tenants/settings",
                    "query": {},
                    "body": {"friendly_name": "[REDACTED]", "picture_url": "[REDACTED]"},
                    "ip": "52.255.188.22",
                    "auth": {
                        "subject": "0K4d0DgZthpVjPgZ2T9lLvqMSqweveLt@clients",
                        "strategy": "jwt_api2_internal_token",
                        "scopes": [
                            "read:authenticators",
                            "remove:authenticators",
                            "update:authenticators",
                            "create:authenticators",
                            "read:enrollments",
                            "delete:enrollments",
                            "read:factors",
                            "update:factors",
                            "update:tenant_settings",
                            "update:users",
                            "create:enrollment_tickets",
                            "create:users",
                        ],
                    },
                },
                "response": {
                    "body": {
                        "name": "agrabah-antunes-dev",
                        "friendly_name": "[REDACTED]",
                        "picture_url": "[REDACTED]",
                        "guardian_mfa_page": "[REDACTED]",
                    },
                    "statusCode": 200,
                },
            },
            "user_id": "0K4d0DgZthpVjPgZ2T9lLvqMSqweveLt@clients",
            "log_id": "90020220511211008911264478356339239018916110206618304530",
        }
        self._post_to_fluentd(body)

    @task
    def informing_mgmt_api_read_management_api_read_operation(self):
        body = {
            "type": "mgmt_api_read",
            "description": "TESTING_PURPOSE",
            "client_id": "UegcnFxLgYbJSVwQEv82cgv9B4Bq6poZ",
            "client_name": "",
            "ip": "35.166.202.113",
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
            "details": {
                "accessedSecrets": ["client_secret"],
                "request": {
                    "method": "get",
                    "path": "/api/v2/clients/VAhX2h3ZWGBUvLglsZu8Wn9ROytMpirq",
                    "query": {},
                    "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                    "body": None,
                    "channel": "https://manage.auth0.com/",
                    "ip": "35.166.202.113",
                    "auth": {
                        "user": {
                            "user_id": "auth0|61e85d76c719b10069a5a28e",
                            "name": "identidade@willianantunes.com",
                            "email": "identidade@willianantunes.com",
                        },
                        "strategy": "jwt",
                        "credentials": {"jti": "b1f3b4ce811ce5b344be398ea41c3eb4"},
                    },
                },
                "response": {"statusCode": 200, "body": {"client_id": "VAhX2h3ZWGBUvLglsZu8Wn9ROytMpirq"}},
            },
            "user_id": "auth0|61e85d76c719b10069a5a28e",
            "log_id": "90020220511183920579927319743435527784119048180122779650",
        }
        self._post_to_fluentd(body)


if __name__ == "__main__":
    run_single_user(Auth0Tenant)
