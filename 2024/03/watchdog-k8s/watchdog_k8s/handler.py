import logging
import sys

from datetime import datetime

import kubernetes.client

from kubernetes import config
from kubernetes.client.rest import ApiException

_logger = logging.getLogger(__name__)
_group = "cert-manager.io"
_version = "v1"


def _create_configuration():
    configuration = kubernetes.client.Configuration()
    # Accessing the API from within a Pod
    # https://kubernetes.io/docs/tasks/run-application/access-api-from-pod/#directly-accessing-the-rest-api
    # https://stackoverflow.com/a/48377444/3899136
    config.load_incluster_config(configuration)
    return configuration


def check_certificates_and_inform_on_slack_if_applicable(certificates: list[str], now=datetime.now().astimezone()):
    _logger.debug("Generating configuration")
    configuration = _create_configuration()

    should_exit = False
    with kubernetes.client.ApiClient(configuration) as client:
        api = kubernetes.client.CustomObjectsApi(client)
        for certificate in certificates:
            _logger.info("Checking certificate: %s", certificate)
            namespace, name = certificate.split("|")
            try:
                api_response = api.get_namespaced_custom_object(_group, _version, namespace, "certificates", name)
            except ApiException as e:
                _logger.error("Exception when calling CustomObjectsApi->get_namespaced_custom_object")
                raise e
            renewal_time = api_response["status"].get("renewalTime")
            if not renewal_time:
                _logger.error("Certificate %s does not have a renewalTime", certificate)
                should_exit = True
                continue
            renewal_time = datetime.fromisoformat(renewal_time)
            if renewal_time <= now:
                _logger.error("Certificate %s is about to expire on %s", certificate, renewal_time)
                should_exit = True
        if should_exit:
            _logger.error("Some certificates are either about to expire or invalid. Please fix them ASAP")
            sys.exit(1)
    _logger.info("Work has been completed")
