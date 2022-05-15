import fileinput
import json
import os
import pathlib

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
auth0_endpoint = f"https://{AUTH0_DOMAIN}/api/v2/"
get_token = GetToken(AUTH0_DOMAIN)


def _yielding_all_matching_files_from_directory(folder, glob_pattern) -> list[Path]:
    return list(pathlib.Path(folder).glob(glob_pattern))


def _refresh_settings(settings_location, key_value_to_replace: Dict[str, str]):
    for line in fileinput.input(settings_location, inplace=True):
        replaced = False
        for key_to_be_found in key_value_to_replace:
            if line.startswith(key_to_be_found):
                value = key_value_to_replace[key_to_be_found]
                replaced = True
                print(f"""{key_to_be_found}={value}\n""", end="")
                break
        if not replaced:
            print(line, end="")


def _load_content_as_string(file_name) -> str:
    with open(file_name, mode="r") as file:
        return "".join(line.rstrip() for line in file)


def _load_content_from_json_file_as_dict(file_path: str):
    file_path = pathlib.Path(file_path)

    with open(file_path, "r") as file:
        return json.load(file)


class UnexpectedBehaviorException(Exception):
    pass


@dataclass(frozen=True)
class ClientDetails:
    client_id: str
    client_secret: str
    name: str
    tenant: str


if __name__ == "__main__":
    print("Getting all env files")
    files = _yielding_all_matching_files_from_directory("./envs", "**/*.env.development")
    assert len(files) == 1, "Two files should have been gotten"
    print("Creating Auth0 Management API Client")
    token = get_token.client_credentials(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, auth0_endpoint)
    auth0 = Auth0(AUTH0_DOMAIN, token["access_token"])
    print("Gathering needed data")
    django_admin, m2m_actions = None, None
    clients = auth0.clients.all(fields=["client_secret", "client_id", "tenant", "name"])
    for client in clients:
        client_name = client["name"].lower()
        if client_name == "Test Django Admin SSO - Regular WebApp".lower():
            django_admin = ClientDetails(**client)
        elif client_name == "Test Django Admin SSO - M2M - Actions".lower():
            m2m_actions = ClientDetails(**client)
    if not django_admin or not m2m_actions:
        raise UnexpectedBehaviorException(
            f"Couldn't find Django Admin ({bool(django_admin)}) or M2M Actions ({bool(m2m_actions)})"
        )
    print("Applying configuration")
    django_admin_keys = {
        "AUTH0_DOMAIN": AUTH0_DOMAIN,
        "AUTH0_APP_CLIENT_ID": django_admin.client_id,
        "AUTH0_APP_CLIENT_SECRET": django_admin.client_secret,
    }
    number_of_updates = 0
    for file in files:
        file_name = str(file)
        if "backend" in file_name:
            _refresh_settings(file, django_admin_keys)
            number_of_updates += 1
    assert number_of_updates == len(files), "I should have updated 1 file. Did I do something wrong? 🤨"
    action_name = "Enrich JWT with Groups from AD"
    actions_pagination = auth0.actions.get_actions(deployed=True, trigger_id="post-login", action_name=action_name)
    action = actions_pagination["actions"][0]
    action_id = action["id"]
    print(f"Action ID: {action_id}")
    body = {
        "secrets": [
            {
                "name": "TENANT",
                "value": AUTH0_DOMAIN,
            },
            {
                "name": "AUDIENCE",
                "value": f"https://{AUTH0_DOMAIN}/api/v2/",
            },
            {
                "name": "APP_CLIENT_ID",
                "value": m2m_actions.client_id,
            },
            {
                "name": "APP_CLIENT_SECRET",
                "value": m2m_actions.client_secret,
            },
        ]
    }
    auth0.actions.update_action(action_id, body)
    print("Done 🥳")
