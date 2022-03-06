import pytest

from jwt import PyJWKClient
from jwt import PyJWKSet
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from authentication_django_rest_framework.apps.core.api.authentication.authentications import (
    JWTAccessTokenAuthentication,
)
from authentication_django_rest_framework.apps.core.api.authentication.models import TokenUser


@pytest.fixture
def jwt_access_token_authentication_scenario(mocker):
    factory = APIRequestFactory()
    # Invalid token create on TOKEN DEV: https://token.dev/
    token_with_invalid_kid = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImRvLXlvdS1saWtlLXNhbHQta2V5LWlkIn0.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkNhcmwgU2FnYW4iLCJhZG1pbiI6dHJ1ZSwiaWF0IjoxNjQ2NjAwNTIxLCJleHAiOjE2NDY2MDQxMjF9.eyrVJEU84OsRUPIhsHpJVTqltn4ITD8LTJbhdgLU20VkDVzZS80u7HsTE_J4Ih4wdxOS3l6jBUOv-6DmBbGkahHM59SBY4aibsIQdGA9s2BWNatl90LpifI4Wjs-0ptkMDVO_i_Pie6RlscThM_jHdj8agi50YTJKRonXjYjLd1wNbleU53tss0ePslh3yynV8lvIjjNT2bSRHpcllh6qFLpiPm_k7K4Ft69oGq3k9BvXCaNGKd5zjsyzP8704aRj0DaXGrqZ-yYwo0FoAGheVl2EKccFn7l4kJTjnwnaeP3eO6FadLjjHS1KEMs6du4AzmSPJSY_T3thV-FmWjekg"
    token_with_valid_kid = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImZhWVp3X0NFSTBJUnotU2FHOWJoaSJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkNhcmwgU2FnYW4iLCJhZG1pbiI6dHJ1ZSwiaWF0IjoxNjQ2NjAwNTIxLCJleHAiOjE2NDY2MDQxMjF9.Obmnybm2oFwC0jOFSrZjVjY3F0W6w1zjCJFwp64rEeLcFa6yTh3zWGqiEtzlCYNGWNg1KS3JkycWqCRDGcsVkFhV1WRiLSHz8kA5m1rEk9A4pl1uSqt3vkGrC7X9h9LkPU2wp4YnCp3fZhIp7Z66rfy1L7Rebu6FyLnM-MFsk6IDikv01kFZkUNFQCYn5Uv1dY3xLWfdnOYllHmOs8boXt5z2DJKtWsNSe7-PBnrW0haQtihrI2cp9jVRj8815r1RBBfVbTQWslAQxdMxvk2ZtxCOvjv3UYG81k-ezVn2zoQXjG-JS4Uox6UQ5j6hR1arF-spkP1mXEtKH3EeB7G-g"
    valid_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZhWVp3X0NFSTBJUnotU2FHOWJoaSJ9.eyJpc3MiOiJodHRwczovL2FudHVuZXMudXMuYXV0aDAuY29tLyIsInN1YiI6ImZhY2Vib29rfDEwMjE4OTI1OTU2NDkxNjQyIiwiYXVkIjpbInVzZXItbWFuYWdlbWVudC9hcGl2aWV3LWRyZi1hcGkvYXBpL3YxIiwiaHR0cHM6Ly9hbnR1bmVzLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NDY2MDI2ODUsImV4cCI6MTY0NjY4OTA4NSwiYXpwIjoiUDRjQkI4YThuMFJybE5FR1c3OWRKbmhBNFpyTVZ5S2oiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIn0.vKE-EdlbSx1KVXenEBkTG62pnUwoWIbHCCoW_Td2rr6pLIbuQzI2XW0lRtVRqlNhVifvFOAkRaascnm24S9_9KFii2IjMYJ4uQ0HpKTC55LgOV1KMkiE-qLS6aSVu5qftWpQmJRQJ9sPoie7siFL8cXznrkWlE4JFtEU4abFkjt5HEbL-BeX_70jrt60til1ImlMuDNmK6g0TiE0Oc6TKilHoRppUE1gN9XFvaaISJLZg5jtYvc-Gj0jeNOsjhyXZaiiCFSCyOZ8VNlZxyJ7EEyRHjVymRNH9vp_u8kKyMzV324Wlzmcbw5tQPUrk3hvnYf3IOT0QM5FFj6AvM228Q"
    fake_jwks = {
        "keys": [
            {
                "alg": "RS256",
                "kty": "RSA",
                "use": "sig",
                "n": "01EW-npmkOYEpwM6LLKpr6OJ1s_gQQz3biUzBY5QdH3JwWS37h6WFUdyv-CJEBWBetbzHLBYx_58HbGcGwmhht7bXJ8WDlRroxvt7MoYhINMaG8aXo3Giw0_st-VaEC8BuNEemfhJHBlcpJR8-ZdSLx5Q-rFojePOdnVrbcGIviVu9b6pOPHI1jnW_WmyBfG5XmXPHy2aL3OxjLFa8uVkxyHIu1mN3hWEdzZqewUqrFe91egCwT7u4MOkLgfmym_meXjXgIJZSp-GvNGJzk8Iyr0EszlrimP8eBgLg4AjEmwQzRkcRSXYsGCjO8-Dy4ecch-YNhOXpzWSf4bC22XYw",
                "e": "AQAB",
                "kid": "faYZw_CEI0IRz-SaG9bhi",
                "x5t": "ovFav4LfCHs4qZaOImYWpxoXdzA",
                "x5c": [
                    "MIIDAzCCAeugAwIBAgIJbqiVa0rLk9wpMA0GCSqGSIb3DQEBCwUAMB8xHTAbBgNVBAMTFGFudHVuZXMudXMuYXV0aDAuY29tMB4XDTIxMTAwNjE1MDIwNVoXDTM1MDYxNTE1MDIwNVowHzEdMBsGA1UEAxMUYW50dW5lcy51cy5hdXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDTURb6emaQ5gSnAzossqmvo4nWz+BBDPduJTMFjlB0fcnBZLfuHpYVR3K/4IkQFYF61vMcsFjH/nwdsZwbCaGG3ttcnxYOVGujG+3syhiEg0xobxpejcaLDT+y35VoQLwG40R6Z+EkcGVyklHz5l1IvHlD6sWiN4852dWttwYi+JW71vqk48cjWOdb9abIF8bleZc8fLZovc7GMsVry5WTHIci7WY3eFYR3Nmp7BSqsV73V6ALBPu7gw6QuB+bKb+Z5eNeAgllKn4a80YnOTwjKvQSzOWuKY/x4GAuDgCMSbBDNGRxFJdiwYKM7z4PLh5xyH5g2E5enNZJ/hsLbZdjAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFC21wXqeOFczGIEjlB+FCDVuaqleMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0BAQsFAAOCAQEAl1I7bmq6ihafH9Zts+Fc9/Pe6kQ6C8yUMTJheNpiX6FTBfEWPuX/KWDz2WcC2/1S8tsQZPD3GJEF899LDa8F+mHY2adWMgFep5e5AejcwdmnZlCZoKmVAZ2HZHMgQr7RM0c0HZ2laBbzv4XcZPiDBP8YCuJlmL4zQFMeuWlA4ShCPB8Vk0VhDIJ/GBHvKYgy2pSa7mfZpoC4JcUc5XV4q6fZahEL27eqC3l4ffXaEcBK1axy769SaJpxHgpEeniMkfGcbuAYamInO64lhqKLf0hq9kQ6WId17hOt9nMa2q2ct88s5ZJirDzkE9uEKr0m9tqqaTgupN/xgq0xHVXkww=="
                ],
            },
            {
                "alg": "RS256",
                "kty": "RSA",
                "use": "sig",
                "n": "uPw-p0UpUVWd54qkPEfxt6GRqt1kJFDmzWmwVBfJxtRLp4m7jixzX9KNQrRWhBNJ1rlAxqpookqeB6cm74aEJ_UAJ-uPHnGKqYdA41VBOMrCgMl-DH86peK-HtGg_0vg6D0qMkcmXZJBGeKdK6UAhw0uwALEqN_twlBwdvtVocS30fvYdt_JqTnSb8uimRnoaA5GoAet5fAG7cph5ZnZuIAYdVf4T3RiPBdRNtHJbP9cuCZatJWb7CabjuIN9wmztAsex8n9wuSp06_wuVWJQQiCDGQF8tT11yn4TlFnzdlwxpQ8ngrvsoAt0KPfA_1rrFBL9vhGIGFkkRvfC3WFUw",
                "e": "AQAB",
                "kid": "1Yjr6qd1riVeCrHC-DuhH",
                "x5t": "oLlrWY6HThi71U-AJZwN4Jn24IU",
                "x5c": [
                    "MIIDAzCCAeugAwIBAgIJU21sCpl+udZDMA0GCSqGSIb3DQEBCwUAMB8xHTAbBgNVBAMTFGFudHVuZXMudXMuYXV0aDAuY29tMB4XDTIxMTAwNjE1MDIwNloXDTM1MDYxNTE1MDIwNlowHzEdMBsGA1UEAxMUYW50dW5lcy51cy5hdXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC4/D6nRSlRVZ3niqQ8R/G3oZGq3WQkUObNabBUF8nG1EunibuOLHNf0o1CtFaEE0nWuUDGqmiiSp4HpybvhoQn9QAn648ecYqph0DjVUE4ysKAyX4Mfzql4r4e0aD/S+DoPSoyRyZdkkEZ4p0rpQCHDS7AAsSo3+3CUHB2+1WhxLfR+9h238mpOdJvy6KZGehoDkagB63l8AbtymHlmdm4gBh1V/hPdGI8F1E20cls/1y4Jlq0lZvsJpuO4g33CbO0Cx7Hyf3C5KnTr/C5VYlBCIIMZAXy1PXXKfhOUWfN2XDGlDyeCu+ygC3Qo98D/WusUEv2+EYgYWSRG98LdYVTAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFG1wVasCVyhsSQnaDuAxSj0AF3/qMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0BAQsFAAOCAQEArfE7/0Khu6Dupfyy9dy5FdL9HUxBF1YgFeOWPBZg8VilRkldjq+S8axYUdbhpyCuEcnnInqO17t+KJ5/oRdEb1Ma4Lj4XD2GdyN1wTniUoq2P/r5aGRqToISAEtwpvVgYmQZflDC9xYq+d5ddZ43LfouWKSkE01OfL7YQJM+yNWm4dwQAT0gXNchnBGRtlajhStYLDb6Sci/AizEIMcqZnkXoBJQXwaEBYZCsXCkWgUoiQFVPzZr07m4iQF4FtoyPsjlbxbhQ2ymEbVCS986zmApkTfv9GcTSpIonoom7fMjkww+7s5/CoKgPCvYeEu+phmW8nzY8o0FsSeNUfI6nw=="
                ],
            },
        ]
    }
    mocked_jwks_client = PyJWKClient("https://agrabah/.well-known/jwks.json")
    mocker.patch.object(mocked_jwks_client, "get_jwk_set", lambda: PyJWKSet.from_dict(fake_jwks))
    extra_internal_options = {
        "internal_extra_jwt_decode_options": {"verify_exp": False},
        "internal_jwks_client": mocked_jwks_client,
    }
    backend = JWTAccessTokenAuthentication(**extra_internal_options)
    return factory, backend, (token_with_invalid_kid, token_with_valid_kid, valid_token)


class TestAccessTokenValidation:
    def test_should_raise_error_if_no_authorization_header_is_available(self):
        # Arrange
        factory = APIRequestFactory()
        request = factory.get("/your-endpoint/v1/salt")
        backend = JWTAccessTokenAuthentication()
        # Act
        with pytest.raises(AuthenticationFailed) as authentication_failed_exception:
            backend.authenticate(request)
        # Assert
        assert authentication_failed_exception.value.status_code == 401
        assert authentication_failed_exception.value.detail == "Authorization header is not present"

    def test_should_raise_error_when_authorization_header_value_is_invalid(self):
        # Arrange
        headers = {
            "HTTP_AUTHORIZATION": "Salt addicted",
        }
        factory = APIRequestFactory()
        request = factory.get("/your-endpoint/v1/salt", **headers)
        backend = JWTAccessTokenAuthentication()
        # Act
        with pytest.raises(AuthenticationFailed) as authentication_failed_exception:
            backend.authenticate(request)
        # Assert
        assert authentication_failed_exception.value.status_code == 401
        assert (
            authentication_failed_exception.value.detail
            == "Authorization header must start with Bearer followed by its token"
        )

    def test_should_raise_error_if_bearer_has_invalid_jwt(self):
        # Arrange
        headers = {
            "HTTP_AUTHORIZATION": "Bearer the-one-where-monica-gets-a-new-roommate",
        }
        factory = APIRequestFactory()
        request = factory.get("/your-endpoint/v1/friends", **headers)
        backend = JWTAccessTokenAuthentication()
        # Act
        with pytest.raises(AuthenticationFailed) as authentication_failed_exception:
            backend.authenticate(request)
        # Assert
        assert authentication_failed_exception.value.status_code == 401
        assert authentication_failed_exception.value.detail == "Bearer does not contain a valid JWT"

    def test_should_raise_error_if_provided_jwt_has_no_kid(self, jwt_access_token_authentication_scenario):
        # Arrange
        factory, backend, tokens = jwt_access_token_authentication_scenario
        token_with_invalid_kid, *_ = tokens
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {token_with_invalid_kid}",
        }
        request = factory.get("/your-endpoint/v1/friends", **headers)
        # Act
        with pytest.raises(AuthenticationFailed) as authentication_failed_exception:
            backend.authenticate(request)
        # Assert
        assert authentication_failed_exception.value.status_code == 401
        assert authentication_failed_exception.value.detail == "JWT does not have a valid Key ID"

    def test_should_raise_error_if_provided_jwt_has_invalid_signature(self, jwt_access_token_authentication_scenario):
        # Arrange
        factory, backend, tokens = jwt_access_token_authentication_scenario
        _, token_with_valid_kid, _ = tokens
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {token_with_valid_kid}",
        }
        request = factory.get("/your-endpoint/v1/friends", **headers)
        # Act
        with pytest.raises(AuthenticationFailed) as authentication_failed_exception:
            backend.authenticate(request)
        # Assert
        assert authentication_failed_exception.value.status_code == 401
        assert authentication_failed_exception.value.detail == "Bearer token is invalid"

    def test_should_return_jwt_user(self, jwt_access_token_authentication_scenario, settings, mocker):
        # Arrange
        settings.AUTH0_MY_APPLICATION_AUDIENCE = "user-management/apiview-drf-api/api/v1"
        mocker.patch(
            "authentication_django_rest_framework.apps.core.api.authentication.authentications.settings", settings
        )
        factory, backend, tokens = jwt_access_token_authentication_scenario
        *_, valid_token = tokens
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {valid_token}",
        }
        request = factory.get("/your-endpoint/v1/friends", **headers)
        expected_token = {
            "iss": "https://antunes.us.auth0.com/",
            "sub": "facebook|10218925956491642",
            "aud": ["user-management/apiview-drf-api/api/v1", "https://antunes.us.auth0.com/userinfo"],
            "iat": 1646602685,
            "exp": 1646689085,
            "azp": "P4cBB8a8n0RrlNEGW79dJnhA4ZrMVyKj",
            "scope": "openid profile email",
        }
        # Act
        result = backend.authenticate(request)
        # Assert
        assert result == (TokenUser(expected_token), expected_token)
