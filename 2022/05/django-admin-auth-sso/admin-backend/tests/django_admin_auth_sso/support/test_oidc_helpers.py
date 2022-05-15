import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from django_admin_auth_sso.support.oidc_helpers import CustomOIDCAuthenticationBackend
from django_admin_auth_sso.support.oidc_helpers import OIDCToDjangoGroupsMapping


def sample_user_info():
    return {
        "sub": "waad|0ukNcu0aWv9Fe05Tn_0K6gDwp_YAWzyQheHF_2_NdgQ",
        "given_name": "Carl",
        "family_name": "Sagan",
        "nickname": "Carl Sagan",
        "name": "Carl Sagan",
        "picture": "https://cdn.auth0.com/avatars/cs.png",
        "updated_at": "2022-04-08T11:01:33.308Z",
        "groups": ["TMP - Iago", "TMP - Cockatiel"],
    }


class TestCustomOIDCAuthenticationBackend:
    @pytest.mark.django_db
    def test_should_create_user(self):
        # Arrange
        oidc_backend = CustomOIDCAuthenticationBackend()
        claims = sample_user_info()
        claims["email"] = "carl.sagan@willianantunes.com"
        # Act
        created_user = oidc_backend.create_user(claims)
        # Assert
        assert created_user
        user_model = get_user_model()
        assert user_model.objects.count() == 1
        attributes = "first_name", "last_name", "email", "username"
        user_with_selected_attributes = get_user_model().objects.values(*attributes)[0]
        assert user_with_selected_attributes == {
            "first_name": claims["given_name"],
            "last_name": claims["family_name"],
            "email": claims["email"],
            "username": claims["sub"],
        }

    @pytest.mark.django_db
    def test_when_having_oidc_payload_should_create_user_with_business_group(self, mocker, settings):
        # Arrange
        oidc_backend = CustomOIDCAuthenticationBackend()
        access_token, id_token, payload = "access_token", "id_token", "payload"
        target_method = "OIDCAuthenticationBackend.get_userinfo"
        mock_get_userinfo = mocker.patch(f"django_admin_auth_sso.support.oidc_helpers.{target_method}")
        claims = sample_user_info()
        mock_get_userinfo.return_value = claims
        groups_claim = "claim-about-grups"
        settings.CUSTOM_OIDC_GROUPS_CLAIM = groups_claim
        mocker.patch("django_admin_auth_sso.support.oidc_helpers.settings", settings)
        claims[groups_claim] = ["B2E_APP_MANAGEMENT_BUSINESS"]
        Group.objects.create(name="business")
        # Act
        assert oidc_backend.get_or_create_user(access_token, id_token, payload)
        # Assert
        assert mock_get_userinfo.call_count == 1
        mock_get_userinfo.assert_called_once_with(access_token, id_token, payload)
        assert get_user_model().objects.count() == 1
        groups_from_created_user = get_user_model().objects.first().groups
        assert groups_from_created_user.count() == 1
        assert groups_from_created_user.get().name == "business"

    @pytest.mark.django_db
    def test_when_having_oidc_payload_should_update_user_with_refreshed_properties(self, mocker):
        # Arrange
        claims = sample_user_info()
        claims["https://www.willianantunes.com/ad/groups"] = ["B2E_APP_MANAGEMENT_VIEWER"]
        user_model = get_user_model()
        user_model.objects.create_user(claims["sub"], first_name="Jack", last_name="Kerouac")
        oidc_backend = CustomOIDCAuthenticationBackend()
        access_token, id_token, payload = "access_token", "id_token", "payload"
        target_method = "OIDCAuthenticationBackend.get_userinfo"
        mock_get_userinfo = mocker.patch(f"django_admin_auth_sso.support.oidc_helpers.{target_method}")
        mock_get_userinfo.return_value = claims
        # Act
        assert oidc_backend.get_or_create_user(access_token, id_token, payload)
        # Assert
        assert mock_get_userinfo.call_count == 1
        mock_get_userinfo.assert_called_once_with(access_token, id_token, payload)
        assert user_model.objects.count() == 1
        attributes = "first_name", "last_name", "email", "username"
        user_with_selected_attributes = user_model.objects.values(*attributes)[0]
        assert user_with_selected_attributes == {
            "first_name": claims["given_name"],
            "last_name": claims["family_name"],
            "email": "",
            "username": claims["sub"],
        }


class TestOIDCToDjangoGroupsMapping:
    def test_should_have_groups_properly_configured(self):
        assert OIDCToDjangoGroupsMapping.oidc_groups_with_django_groups == [
            ("B2E_APP_MANAGEMENT_VIEWER", "viewer"),
            ("B2E_APP_MANAGEMENT_SUPPORT", "support"),
            ("B2E_APP_MANAGEMENT_BUSINESS", "business"),
            ("B2E_APP_MANAGEMENT_DEVELOPER", "developer"),
        ]

    def test_should_check_valid_groups(self):
        # Arrange
        valid_groups = [
            "B2E_APP_MANAGEMENT_VIEWER",
            "B2E_APP_MANAGEMENT_SUPPORT",
            "B2E_APP_MANAGEMENT_BUSINESS",
            "B2E_APP_MANAGEMENT_DEVELOPER",
        ]
        invalid_groups = [
            "JAFAR",
            "IAGO",
            "ALADDIN",
            "SALT",
        ]
        # Act and assert
        assert OIDCToDjangoGroupsMapping.has_any_valid_group(invalid_groups) is False
        assert OIDCToDjangoGroupsMapping.has_any_valid_group(valid_groups) is True

    @pytest.mark.django_db
    def test_should_retrieve_one_django_group(self):
        # Arrange
        viewer_group = Group.objects.create(name="viewer")
        groups = ["B2E_APP_MANAGEMENT_VIEWER"]
        # Act
        django_groups = OIDCToDjangoGroupsMapping.retrieve_django_groups(groups)
        # Assert
        assert django_groups.count() == 1
        assert django_groups.first() == viewer_group

    @pytest.mark.django_db
    def test_should_retrieve_two_django_group(self):
        # Arrange
        business_group = Group.objects.create(name="business")
        support_group = Group.objects.create(name="support")
        groups = ["B2E_APP_MANAGEMENT_BUSINESS", "B2E_APP_MANAGEMENT_SUPPORT"]
        # Act
        django_groups = OIDCToDjangoGroupsMapping.retrieve_django_groups(groups)
        # Assert
        assert django_groups.count() == 2
        assert django_groups.get(name=business_group.name) == business_group
        assert django_groups.get(name=support_group.name) == support_group
