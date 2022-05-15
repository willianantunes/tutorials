from django.contrib.auth.models import Group
from django.db.models import QuerySet
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from django_admin_auth_sso import settings
from django_admin_auth_sso.support.http_utils import build_url_with_query_strings


def provider_logout(request):
    params = {
        "returnTo": settings.LOGOUT_REDIRECT_URL,
        "client_id": settings.OIDC_RP_CLIENT_ID,
    }
    return build_url_with_query_strings(settings.AUTH0_LOGOUT_ENDPOINT, params)


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims) -> bool:
        groups = self._retrieve_groups_from_claims(claims)
        return OIDCToDjangoGroupsMapping.has_any_valid_group(groups)

    def create_user(self, claims):
        # Basic attributes
        user_id = claims["sub"]
        email = claims.get("email")
        given_name = claims.get("given_name")
        family_name = claims.get("family_name")
        # User creation
        created_user = self.UserModel.objects.create_user(
            user_id,
            email=email,
            first_name=given_name,
            last_name=family_name,
            is_staff=True,
        )
        # Relationships
        self._fill_user_with_groups(created_user, claims)
        created_user.save()
        return created_user

    def update_user(self, user, claims):
        # Basic attributes
        given_name = claims.get("given_name")
        family_name = claims.get("family_name")
        # User update
        user.first_name = given_name
        user.last_name = family_name
        # Relationships
        self._fill_user_with_groups(user, claims)
        user.save()
        return user

    def filter_users_by_claims(self, claims):
        qs_users = super().filter_users_by_claims(claims)
        if not qs_users:
            user_id = claims["sub"]
            return self.UserModel.objects.filter(username__iexact=user_id)
        return qs_users

    @staticmethod
    def _retrieve_groups_from_claims(claims: dict):
        return claims.get(settings.CUSTOM_OIDC_GROUPS_CLAIM, [])

    @classmethod
    def _fill_user_with_groups(cls, user, claims):
        groups = cls._retrieve_groups_from_claims(claims)
        django_groups = OIDCToDjangoGroupsMapping.retrieve_django_groups(groups)
        user.groups.set(django_groups)


class OIDCToDjangoGroupsMapping:
    oidc_groups_with_django_groups = [
        ("B2E_APP_MANAGEMENT_VIEWER", "viewer"),
        ("B2E_APP_MANAGEMENT_SUPPORT", "support"),
        ("B2E_APP_MANAGEMENT_BUSINESS", "business"),
        ("B2E_APP_MANAGEMENT_DEVELOPER", "developer"),
    ]

    @classmethod
    def retrieve_django_groups(cls, groups: list[str]) -> QuerySet:
        selected_groups = cls._retrieve_django_groups(groups)
        return Group.objects.filter(name__in=selected_groups)

    @classmethod
    def has_any_valid_group(cls, groups: list[str]) -> bool:
        return any(cls._retrieve_django_groups(groups))

    @classmethod
    def _retrieve_django_groups(cls, groups: list[str]):
        django_groups = []

        for oidc_group, django_group in cls.oidc_groups_with_django_groups:
            is_group_configured = oidc_group in groups
            if is_group_configured:
                django_groups.append(django_group)

        return django_groups
