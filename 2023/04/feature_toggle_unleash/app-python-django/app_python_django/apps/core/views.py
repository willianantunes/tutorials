import json
import logging

from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from app_python_django.apps.core.models import Profile
from app_python_django.apps.core.providers.feature_management import client

logger = logging.getLogger(__name__)


def index(request):
    user_id_pc = "40956364-e486-4d8e-b35e-60660721f467"
    user_id_mobile = "d821cbc0-2e4d-49fc-a5b4-990eb991beec"
    user_id = user_id_pc if request.user_agent.is_pc else user_id_mobile
    user_context = {
        "userId": user_id,
        # Browser family can be `chrome` or `firefox`
        "browser": request.user_agent.browser.family.lower(),
    }

    # `PERMISSION` TOGGLES
    should_show_profiles = client.is_enabled("SHOW_PROFILES", context=user_context)
    should_allow_profile_management = client.is_enabled("ALLOW_PROFILE_MANAGEMENT", context=user_context)
    # `EXPERIMENT` TOGGLES
    profile_management_button_scheme = client.get_variant("PROFILE_MANAGEMENT_BUTTON_SCHEME", context=user_context)
    if profile_management_button_scheme["enabled"]:
        button_scheme_name = profile_management_button_scheme["name"]
        button_scheme_value = profile_management_button_scheme["payload"]["value"]
    else:
        button_scheme_name = "FALLBACK"
        button_scheme_value = "btn-danger"
    logger.info("Using the button scheme %s with value %s", button_scheme_name, button_scheme_value)
    text_presentation = client.get_variant("TEXT_PRESENTATION", context=user_context)
    if text_presentation["enabled"]:
        text_presentation_name = text_presentation["name"]
        text_presentation_value = json.loads(text_presentation["payload"]["value"])
    else:
        text_presentation_name = "FALLBACK"
        text_presentation_value = {
            "title": "Hello there 😄!",
            "subTitle": "Change how this app behave by changing the feature toggle tool ⚒",
            "profileTitle": "Registered profiles",
        }
    logger.info("Using the text presentation %s with value %s", text_presentation_name, text_presentation_value)
    # `KILL-SWITCH TOGGLES
    game_shark_mode = client.is_enabled("GAME_SHARK_MODE", context=user_context)

    context = {
        "show_profiles": should_show_profiles,
        "allow_profile_management": should_allow_profile_management,
        "button_scheme_value": button_scheme_value,
        "text_presentation": text_presentation_value,
        "game_shark_mode": game_shark_mode,
        "profiles": Profile.objects.all(),
    }

    return render(request, "core/pages/home.html", context)


def manage_profiles(request):
    redirect_uri = _build_uri(request, "index")

    if request.method == "POST" and request.POST.get("method") == "DELETE":
        profile_id = request.POST["profileId"]
        Profile.objects.get(id=profile_id).delete()

    return redirect(redirect_uri)


def _build_uri(request, view_name):
    location_redirect = reverse(view_name)
    return request.build_absolute_uri(location_redirect)
