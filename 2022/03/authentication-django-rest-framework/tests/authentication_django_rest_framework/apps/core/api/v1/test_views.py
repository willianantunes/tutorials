import pytest


@pytest.fixture
def accept_fake_access_token(mocker):
    mock_class = mocker.patch(
        "authentication_django_rest_framework.apps.core.api.authentication.authentications.PyJWKClient"
    )
    mock_class.return_value = mocker.MagicMock()
    mocked_jwt = mocker.patch("authentication_django_rest_framework.apps.core.api.authentication.authentications.jwt")
    fake_data = {
        "iss": "https://antunes.us.auth0.com/",
        "sub": "facebook|10218925956491642",
        "aud": ["user-management/apiview-drf-api/api/v1", "https://antunes.us.auth0.com/userinfo"],
        "iat": 1646602685,
        "exp": 1646689085,
        "azp": "P4cBB8a8n0RrlNEGW79dJnhA4ZrMVyKj",
        "scope": "openid profile email",
    }
    mocked_jwt.decode.return_value = fake_data
    return fake_data


class TestExampleView:
    def test_should_return_200_with_user_attributes(self, accept_fake_access_token, client):
        # Arrange
        token_body = accept_fake_access_token
        header = {
            "HTTP_AUTHORIZATION": "Bearer you-should-watch-arcane",
        }
        # Act
        response = client.get("/api/v1/friends", content_type="application/json", **header)
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result == {"user": token_body["sub"]}
