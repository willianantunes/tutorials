import fileinput
import json
import shlex
import subprocess

from typing import Dict
from typing import List
from typing import Union


def execute_command(command: Union[List[str], str]) -> Union[bytes, str]:
    subprocess_params = {"capture_output": True, "encoding": "utf8", "cwd": "cognito_iac"}
    if type(command) is not str:
        return subprocess.run(command, **subprocess_params).stdout
    else:
        process_list = list()
        previous_process = None
        for command_part in command.split("|"):
            args = shlex.split(command_part)
            if previous_process is None:
                process = subprocess.Popen(args, stdout=subprocess.PIPE)
            else:
                process = subprocess.Popen(args, stdin=previous_process.stdout, stdout=subprocess.PIPE)
            process_list.append(process)
            previous_process = process
        last_process = process_list[-1]
        output, errors = last_process.communicate()
        assert errors is None
        return output.decode("utf-8", "ignore")


def refresh_settings(settings_location: str, key_value_to_replace: Dict[str, str]):
    for line in fileinput.input(settings_location, inplace=True):
        replaced = False
        for key_to_be_found in key_value_to_replace:
            if line.startswith(key_to_be_found):
                value = key_value_to_replace[key_to_be_found]
                replaced = True
                print(f"""{key_to_be_found} = "{value}"\n""", end="")
                break
        if not replaced:
            print(line, end="")


def gpg_decrypt(encrypted_value: str, passphrase: str):
    # Look at for more details here: https://unix.stackexchange.com/a/415064
    first_command = f"echo {encrypted_value}"
    second_command = "base64 -d"
    third_command = f"gpg -d --pinentry-mode loopback --passphrase {passphrase}"
    command_to_retrieve_decrypted_value = "|".join([first_command, second_command, third_command])
    return execute_command(command_to_retrieve_decrypted_value)


if __name__ == "__main__":
    command_to_retrieve_cognito_details = ["terraform", "output", "-json"]
    json_result = execute_command(command_to_retrieve_cognito_details)
    cognito_details = json.loads(json_result)
    # Cognito User Pool
    user_pool_details = cognito_details["cognito_user_pool"]["value"]["user_pool"]
    user_pool_id = user_pool_details["id"]
    # Clients
    product_a_client_id, product_a_client_secret = (
        cognito_details["cognito_clients"]["value"]["poc-product-a-appclientcognito-tmp"]["id"],
        cognito_details["cognito_client_secrets"]["value"]["poc-product-a-appclientcognito-tmp"],
    )
    product_b_client_id, product_b_client_secret = (
        cognito_details["cognito_clients"]["value"]["poc-product-b-appclientcognito-tmp"]["id"],
        cognito_details["cognito_client_secrets"]["value"]["poc-product-b-appclientcognito-tmp"],
    )
    functional_testing_access_key, functional_testing_encrypted_secret = (
        cognito_details["iam_encrypted_access_keys"]["value"]["poc-cognito-custom-ui-api"]["access_key"],
        cognito_details["iam_encrypted_access_keys"]["value"]["poc-cognito-custom-ui-api"]["encrypted_secret"],
    )
    functional_testing_secret_key = gpg_decrypt(functional_testing_encrypted_secret, "YOUR-PASSPHRASE")
    # Configure product A
    where_settings_is_product_a = "product_a/product_a/settings.py"
    find_key_and_replace_for_value_product_a = {
        "AWS_COGNITO_USER_POOL_ID": user_pool_id,
        "AWS_COGNITO_APP_CLIENT_ID": product_a_client_id,
        "AWS_COGNITO_APP_CLIENT_SECRET": product_a_client_secret,
    }
    refresh_settings(where_settings_is_product_a, find_key_and_replace_for_value_product_a)
    # Configure product B
    where_settings_is_product_b = "product_b/product_b/settings.py"
    find_key_and_replace_for_value_product_b = {
        "AWS_COGNITO_USER_POOL_ID": user_pool_id,
        "AWS_COGNITO_APP_CLIENT_ID": product_b_client_id,
        "AWS_COGNITO_APP_CLIENT_SECRET": product_b_client_secret,
    }
    refresh_settings(where_settings_is_product_b, find_key_and_replace_for_value_product_b)
    # Configure functional testing
    where_settings_is_functional_testing = "functional_testing/tests/settings.py"
    find_key_and_replace_for_value_functional_testing = {
        "AWS_COGNITO_USER_POOL_ID": user_pool_id,
        "AWS_COGNITO_SERVICE_ACCOUNT_ACCESS_KEY": functional_testing_access_key,
        "AWS_COGNITO_SERVICE_ACCOUNT_ACCESS_SECRET": functional_testing_secret_key,
        "AWS_COGNITO_APP_CLIENT_ID": product_a_client_id,
        "AWS_COGNITO_APP_CLIENT_SECRET": product_a_client_secret,
    }
    refresh_settings(where_settings_is_functional_testing, find_key_and_replace_for_value_functional_testing)
