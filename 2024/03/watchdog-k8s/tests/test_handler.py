import unittest

from datetime import datetime
from datetime import timedelta
from unittest.mock import MagicMock
from unittest.mock import patch

from watchdog_k8s.handler import check_certificates_and_inform_on_slack_if_applicable


class TestHandler(unittest.TestCase):
    @patch("watchdog_k8s.handler._create_configuration")
    @patch("watchdog_k8s.handler.kubernetes.client")
    def test_should_do_nothing_given_certificate_is_not_about_to_expire(self, mock_client, mock_create_configuration):
        # Arrange
        mock_class_custom_object_api = mock_client.CustomObjectsApi
        mock_api = MagicMock()
        mock_class_custom_object_api.return_value = mock_api
        mock_api.get_namespaced_custom_object.return_value = {
            "status": {
                "renewalTime": (datetime.now().astimezone() + timedelta(days=30)).isoformat(),
            },
        }
        certificates = ["proxies|develop-willianantunesi-com-br"]
        # Act
        check_certificates_and_inform_on_slack_if_applicable(certificates)
        # Assert
        mock_create_configuration.assert_called_once()
        mock_api.get_namespaced_custom_object.assert_called_once_with(
            "cert-manager.io", "v1", "proxies", "certificates", certificates[0].split("|")[1]
        )

    @patch("watchdog_k8s.handler._create_configuration")
    @patch("watchdog_k8s.handler.kubernetes.client")
    def test_should_exit_given_certificate_is_about_to_expire(self, mock_client, mock_create_configuration):
        # Arrange
        mock_class_custom_object_api = mock_client.CustomObjectsApi
        mock_api = MagicMock()
        mock_class_custom_object_api.return_value = mock_api
        fake_now = datetime.fromisoformat("2024-04-25T13:04:35Z")
        mock_api.get_namespaced_custom_object.return_value = {
            "status": {
                "renewalTime": "2024-04-25T13:04:35Z",
            },
        }
        certificates = ["proxies|develop-willianantunesi-com-br"]
        # Act
        with self.assertRaises(SystemExit) as e:
            check_certificates_and_inform_on_slack_if_applicable(certificates, fake_now)
        # Assert
        mock_create_configuration.assert_called_once()
        mock_api.get_namespaced_custom_object.assert_called_once_with(
            "cert-manager.io", "v1", "proxies", "certificates", certificates[0].split("|")[1]
        )
        the_exception = e.exception
        self.assertEqual(the_exception.code, 1)
