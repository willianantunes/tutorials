import argparse

from urllib.parse import quote

import requests

from requests.auth import HTTPBasicAuth

from settings import TARGET_EXCHANGE
from settings import TARGET_ROUTING_KEY


# Based on the library: https://github.com/deslum/pyrabbit2/blob/master/pyrabbit2/api.py
class RabbitMQManagementAPI:
    urls = {
        "overview": "overview",
        "all_queues": "queues",
        "all_exchanges": "exchanges",
        "all_channels": "channels",
        "all_connections": "connections",
        "all_nodes": "nodes",
        "all_vhosts": "vhosts",
        "all_users": "users",
        "all_permissions": "permissions",
        "all_bindings": "bindings",
        "whoami": "whoami",
        "queues_by_vhost": "queues/%s",
        "queues_by_name": "queues/%s/%s",
        "queue_action": "queues/%s/%s/actions",
        "exchanges_by_vhost": "exchanges/%s",
        "exchange_by_name": "exchanges/%s/%s",
        "live_test": "aliveness-test/%s",
        "purge_queue": "queues/%s/%s/contents",
        "channels_by_name": "channels/%s",
        "connections_by_name": "connections/%s",
        "bindings_by_source_exch": "exchanges/%s/%s/bindings/source",
        "bindings_by_dest_exch": "exchanges/%s/%s/bindings/destination",
        "bindings_on_queue": "queues/%s/%s/bindings",
        "bindings_between_exch_queue": "bindings/%s/e/%s/q/%s",
        "bindings_between_exch_exch": "bindings/%s/e/%s/e/%s",
        "rt_bindings_between_exch_queue": "bindings/%s/e/%s/q/%s/%s",
        "rt_bindings_between_exch_exch": "bindings/%s/e/%s/e/%s/%s",
        "get_from_queue": "queues/%s/%s/get",
        "publish_to_exchange": "exchanges/%s/%s/publish",
        "vhosts_by_name": "vhosts/%s",
        "vhost_permissions": "permissions/%s/%s",
        "users_by_name": "users/%s",
        "user_permissions": "users/%s/permissions",
        "vhost_permissions_get": "vhosts/%s/permissions",
        "shovel": "parameters/shovel/%s/%s",
        "all_shovels": "parameters/shovel",
        "policy": "policies/%s/%s",
        "all_policies": "policies",
        "definitions": "definitions",
        "extensions": "extensions",
        "cluster-name": "cluster-name",
    }

    def __init__(self, endpoint, user, password):
        self.endpoint = endpoint
        self.auth = HTTPBasicAuth(user, password)

    def create_queue(self, vhost, name, arguments=None, durable=True):
        vhost = quote(vhost, "")
        name = quote(name, "")
        path = self.urls["queues_by_name"] % (vhost, name)
        endpoint = f"{self.endpoint}/{path}"
        body = {
            "vhost": vhost,
            "name": name,
            "durable": durable,
            "arguments": arguments or {},
        }
        response = requests.put(endpoint, auth=self.auth, json=body)
        response.raise_for_status()

    def delete_queue(self, vhost, name):
        vhost = quote(vhost, "")
        qname = quote(name, "")
        path = self.urls["queues_by_name"] % (vhost, qname)
        endpoint = f"{self.endpoint}/{path}"
        response = requests.delete(endpoint, auth=self.auth)
        if response.status_code == 404:
            return
        response.raise_for_status()

    def create_binding(self, vhost, exchange, queue, routing_key, arguments=None):
        vhost = quote(vhost, "")
        exchange = quote(exchange, "")
        queue = quote(queue, "")
        body = {
            "vhost": vhost,
            "destination": queue,
            "destination_type": "q",
            "source": exchange,
            "routing_key": routing_key,
            "arguments": arguments or {},
        }
        path = self.urls["bindings_between_exch_queue"] % (vhost, exchange, queue)
        endpoint = f"{self.endpoint}/{path}"
        response = requests.post(endpoint, json=body, auth=self.auth)
        response.raise_for_status()

    def create_exchange(self, vhost, name, xtype, auto_delete=False, durable=True, internal=False, arguments=None):
        vhost = quote(vhost, "")
        name = quote(name, "")
        path = self.urls["exchange_by_name"] % (vhost, name)
        endpoint = f"{self.endpoint}/{path}"
        body = {
            "type": xtype,
            "auto_delete": auto_delete,
            "durable": durable,
            "internal": internal,
            "arguments": arguments or list(),
        }
        response = requests.put(endpoint, auth=self.auth, json=body)
        response.raise_for_status()

    def delete_exchange(self, vhost, name):
        vhost = quote(vhost, "")
        name = quote(name, "")
        path = self.urls["exchange_by_name"] % (vhost, name)
        endpoint = f"{self.endpoint}/{path}"
        response = requests.delete(endpoint, auth=self.auth)
        if response.status_code == 404:
            return
        response.raise_for_status()

    def create_policy(self, vhost: str, policy_name: str, pattern: str, apply_to: str, priority: int, definition: dict):
        vhost = quote(vhost, "")
        policy_name = quote(policy_name, "")
        body = {
            "vhost": vhost,
            "name": policy_name,
            "pattern": pattern,
            "apply-to": apply_to,
            "priority": priority,
            "definition": definition,
        }
        path = self.urls["policy"] % (vhost, policy_name)
        endpoint = f"{self.endpoint}/{path}"
        response = requests.put(endpoint, auth=self.auth, json=body)
        response.raise_for_status()


def create_alternate_exchange_environment(api, vhost, name):
    alternate_exchange_name = f"unrouted.{name}"
    api.create_policy(
        vhost=vhost,
        policy_name=f"Default AE: {alternate_exchange_name}",
        pattern=f"^{name}$",
        apply_to="exchanges",
        priority=100,
        definition={"alternate-exchange": alternate_exchange_name},
    )
    api.create_exchange(vhost, alternate_exchange_name, xtype="fanout")
    queue_name = f"listener.unrouted.{name}"
    api.create_queue(vhost, queue_name)
    api.create_binding(vhost, alternate_exchange_name, queue_name, "fanout-ignores-routing-key")


def delete_alternate_exchange_environment(api, vhost, name):
    queue_name = f"listener.unrouted.{name}"
    api.delete_queue(vhost, queue_name)
    alternate_exchange_name = f"unrouted.{name}"
    api.delete_exchange(vhost, alternate_exchange_name)


def create_queue(api: RabbitMQManagementAPI, vhost, exchange, queue_name, routing_key):
    api.create_queue(vhost, queue_name)
    api.create_binding(vhost, exchange, queue_name, routing_key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--delete-queue-by-name")
    args = parser.parse_args()
    delete_queue_by_name = args.delete_queue_by_name
    target_vhost = "/"
    target_api = RabbitMQManagementAPI("http://rabbitmq:15672/api", "guest", "guest")
    if delete_queue_by_name:
        print(f"Deleting queue {delete_queue_by_name}")
        target_api.delete_queue(target_vhost, delete_queue_by_name)
    else:
        target_exchanges_you_want_to_listen = [
            "purchase",
            "shipping",
            TARGET_EXCHANGE,
        ]
        print("Creating alternate exchanges and queues for unrouted messages")
        for target_exchange in target_exchanges_you_want_to_listen:
            print(f"Creating alternate exchange for {target_exchange}")
            delete_alternate_exchange_environment(target_api, target_vhost, target_exchange)
            create_alternate_exchange_environment(target_api, target_vhost, target_exchange)
        print("Creating the EXCHANGE and a queue to test the policy and see how it works by practice")
        target_api.delete_exchange(target_vhost, TARGET_EXCHANGE)
        testing_queue_name = f"listener.{TARGET_EXCHANGE}"
        target_api.delete_queue(target_vhost, testing_queue_name)
        target_api.create_exchange(target_vhost, TARGET_EXCHANGE, xtype="direct")
        create_queue(target_api, target_vhost, TARGET_EXCHANGE, f"listener.{TARGET_EXCHANGE}", TARGET_ROUTING_KEY)
