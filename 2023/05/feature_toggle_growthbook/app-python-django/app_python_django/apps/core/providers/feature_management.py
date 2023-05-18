import logging

from uuid import uuid4

from django.conf import settings
from growthbook import GrowthBook

from app_python_django.support.local_threading_utils import add_to_local_threading
from app_python_django.support.local_threading_utils import get_from_local_threading
from app_python_django.support.local_threading_utils import remove_from_local_threading

_logger = logging.getLogger(__name__)


def setting(name, default=None):
    """
    Helper function to get a Django setting by name. If setting doesn't exist it will return a default.
    """
    return getattr(settings, name, default)


class FeatureManagementMiddleware:
    client_key = "client-key-threading"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._before_calling_view(request)
        response = self.get_response(request)
        self._after_calling_view(request)
        return response

    def _before_calling_view(self, request):
        user_id_pc = "40956364-e486-4d8e-b35e-60660721f467"
        user_id_mobile = "d821cbc0-2e4d-49fc-a5b4-990eb991beec"
        user_id = user_id_pc if request.user_agent.is_pc else user_id_mobile
        browser = request.user_agent.browser.family.lower()
        if browser == "firefox":
            # Just to mimic random users as there is no such option on GrowthBook
            user_id = str(uuid4())
        user_context = {
            "userId": user_id,
            "browser": browser,
        }
        cnpj = request.session.get("cnpj")
        if cnpj:
            user_context["cnpj"] = cnpj
        client = GrowthBook(
            attributes=user_context,
            api_host=setting("GROWTHBOOK_URL"),
            client_key=setting("GROWTHBOOK_CLIENT_KEY"),
        )
        client.load_features()
        add_to_local_threading(self.client_key, client)

    def _after_calling_view(self, request):
        client: GrowthBook = get_from_local_threading(self.client_key)
        client.destroy()
        remove_from_local_threading(self.client_key)


def retrieve_client() -> GrowthBook:
    return get_from_local_threading(FeatureManagementMiddleware.client_key)
