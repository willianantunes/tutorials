import json
import logging

from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from app_python_django.apps.core.models import Profile
from app_python_django.apps.core.providers.feature_management import retrieve_client

logger = logging.getLogger(__name__)


def index(request):
    client = retrieve_client()
    # `PERMISSION` TOGGLES
    should_show_profiles = client.is_enabled("SHOW_PROFILES")
    should_allow_profile_management = client.is_enabled("ALLOW_PROFILE_MANAGEMENT")
    # `EXPERIMENT` TOGGLES
    your_are_special = client.is_enabled("YOU_ARE_SPECIAL_FOR_US")
    profile_management_button_scheme = client.get_variant("PROFILE_MANAGEMENT_BUTTON_SCHEME")
    if profile_management_button_scheme["enabled"]:
        button_scheme_name = profile_management_button_scheme["name"]
        button_scheme_value = profile_management_button_scheme["payload"]["value"]
    else:
        button_scheme_name = "FALLBACK"
        button_scheme_value = "btn-danger"
    logger.info("Using the button scheme %s with value %s", button_scheme_name, button_scheme_value)
    text_presentation = client.get_variant("TEXT_PRESENTATION")
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
    game_shark_mode = client.is_enabled("GAME_SHARK_MODE")

    context = {
        "show_profiles": should_show_profiles,
        "allow_profile_management": should_allow_profile_management,
        "your_are_special": your_are_special,
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


def define_cnpj(request):
    redirect_uri = _build_uri(request, "index")

    if request.method == "POST":
        request.session["cnpj"] = request.POST["inputCnpj"]

    return redirect(redirect_uri)


def _build_uri(request, view_name):
    location_redirect = reverse(view_name)
    return request.build_absolute_uri(location_redirect)
