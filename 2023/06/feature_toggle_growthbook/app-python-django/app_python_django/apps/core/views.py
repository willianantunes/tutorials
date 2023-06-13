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
    should_show_profiles = client.is_on("SHOW_PROFILES".lower())
    should_allow_profile_management = client.is_on("ALLOW_PROFILE_MANAGEMENT".lower())
    # `EXPERIMENT` TOGGLES
    your_are_special = client.is_on("YOU_ARE_SPECIAL_FOR_US".lower())
    button_scheme_value = client.get_feature_value("PROFILE_MANAGEMENT_BUTTON_SCHEME".lower(), "btn-danger")
    logger.info("Using the value %s for PROFILE_MANAGEMENT_BUTTON_SCHEME", button_scheme_value)
    text_presentation = client.get_feature_value(
        "TEXT_PRESENTATION".lower(),
        {
            "title": "Hello there 😄!",
            "subTitle": "Change how this app behave by changing the feature toggle tool ⚒",
            "profileTitle": "Registered profiles",
        },
    )
    logger.info("Using the value %s for TEXT_PRESENTATION", text_presentation)
    # `KILL-SWITCH TOGGLES
    game_shark_mode = client.is_on("GAME_SHARK_MODE".lower())

    context = {
        "show_profiles": should_show_profiles,
        "allow_profile_management": should_allow_profile_management,
        "your_are_special": your_are_special,
        "button_scheme_value": button_scheme_value,
        "text_presentation": text_presentation,
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
