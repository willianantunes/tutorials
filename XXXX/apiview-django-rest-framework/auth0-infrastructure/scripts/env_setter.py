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
    assert len(files) == 2, "Two files should have been gotten"
    print("Creating Auth0 Management API Client")
    token = get_token.client_credentials(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, auth0_endpoint)
    auth0 = Auth0(AUTH0_DOMAIN, token["access_token"])
    print("Gathering needed data")
    django_api, product_xyz = None, None
    clients = auth0.clients.all(fields=["client_secret", "client_id", "tenant", "name"])
    for client in clients:
        client_name = client["name"].lower()
        if client_name == "Test - User Management - APIView DRF API".lower():
            django_api = ClientDetails(**client)
        elif client_name == "Product XYZ".lower():
            product_xyz = ClientDetails(**client)
    if not django_api or not product_xyz:
        raise UnexpectedBehaviorException("Couldn't find Django API or Product XYZ")
    print("Applying configuration")
    django_api_audience = "user-management/apiview-drf-api/api/v1"
    django_api_keys = {
        "AUTH0_DOMAIN": AUTH0_DOMAIN,
        "AUTH0_MY_APPLICATION_AUDIENCE": django_api_audience,
        "AUTH0_MY_APPLICATION_KEY": django_api.client_id,
        "AUTH0_MY_APPLICATION_SECRET": django_api.client_secret,
    }
    product_xyz = {
        "NEXT_PUBLIC_IDP_DOMAIN": AUTH0_DOMAIN,
        "NEXT_PUBLIC_IDP_CLIENT_ID": product_xyz.client_id,
        "NEXT_PUBLIC_IDP_BACKEND_USER_MANAGEMENT_AUDIENCE": django_api_audience,
    }
    number_of_updates = 0
    for file in files:
        file_name = str(file)
        if "backend" in file_name:
            _refresh_settings(file, django_api_keys)
            number_of_updates += 1
        if "frontend" in file_name:
            _refresh_settings(file, product_xyz)
            number_of_updates += 1
    assert number_of_updates == 2, "I should have updated 2 files. Did I do something wrong? 🤨"
    print("Done 🥳")
