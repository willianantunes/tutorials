import unittest

from uuid import uuid4

from common.feature_management import AdminUnleash


class TestAdminUnleash(unittest.TestCase):
    def test_should_create_api_token(self):
        # Arrange
        address = "http://localhost:4242"
        token = "*:*.259035f2b265400b5b7ed759346e2cac13b3ac5089664a29fc6e22a0"
        admin_client = AdminUnleash(address, token)
        username = f"app-test-{uuid4()}"
        client_type = "client"
        # Act
        response = admin_client.create_api_token(username, client_type)
        # Assert
        self.assertEqual(
            {
                "username": "app-test-597ce753-b2cb-4842-ac20-bf6b86a29b8e",
                "type": "client",
                "environment": "development",
                "projects": ["default"],
                "secret": "default:development.106e0c28dac4f04a0f16709f34017649eb6d953416c95c61d2fe2673",
                "alias": None,
                "project": "default",
                "createdAt": "2023-05-26T13:57:22.724Z",
            },
            response,
        )
