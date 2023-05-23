import logging

from UnleashClient import UnleashClient


def setting(name, default=None):
    from django.conf import settings

    """
    Helper function to get a Django setting by name. If setting doesn't exist it will return a default.
    """
    return getattr(settings, name, default)


class Client:
    def __init__(self):
        custom_headers = setting("UNLEASH_CUSTOM_HEADERS")
        custom_options = setting("UNLEASH_CUSTOM_OPTIONS")
        custom_strategies = setting("UNLEASH_CUSTOM_STRATEGIES")

        self._url = setting("UNLEASH_URL")
        self._app_name = setting("UNLEASH_APP_NAME")
        self._environment = setting("UNLEASH_ENVIRONMENT", "default")
        self._instance_id = setting("UNLEASH_INSTANCE_ID", "unleash-client-python")
        self._refresh_interval = setting("UNLEASH_INTERVAL_RATE", 5)
        self._refresh_jitter = setting("UNLEASH_REFRESH_JITTER", None)
        self._metrics_interval = setting("UNLEASH_METRICS_INTERVAL", 10)
        self._metrics_jitter = setting("UNLEASH_METRICS_JITTER", None)
        self._disable_metrics = setting("UNLEASH_DISABLE_METRICS", False)
        self._disable_registration = setting("UNLEASH_DISABLE_REGISTRATION", False)
        self._custom_headers = custom_headers or {}
        self._custom_options = custom_options or {}
        self._custom_strategies = custom_strategies or {}
        self._cache_directory = setting("UNLEASH_CACHE_DIRECTORY")
        self._project_name = setting("UNLEASH_PROJECT_NAME")
        # https://docs.getunleash.io/unleash-client-python/usage.html#logging
        self._verbose_log_level = setting("UNLEASH_VERBOSE_LOG_LEVEL", logging.WARNING)
        self._cache = setting("UNLEASH_CACHE")
        self._token = setting("UNLEASH_API_TOKEN")
        self._fake_initialize = setting("UNLEASH_FAKE_INITIALIZE", False)

    def _update_custom_header(self):
        auth_header = {
            "Authorization": self._token,
        }
        return self._custom_headers.update(auth_header)

    def _set_log_severity(self):
        for logger_name in ["UnleashClient", "apscheduler.scheduler", "apscheduler.executors"]:
            logging.getLogger(logger_name).setLevel(self._verbose_log_level)

    def connect(self) -> UnleashClient:
        self._update_custom_header()
        self._set_log_severity()

        unleash_client = UnleashClient(
            url=self._url,
            app_name=self._app_name,
            custom_headers=self._custom_headers,
            environment=self._environment,
            instance_id=self._instance_id,
            refresh_interval=self._refresh_interval,
            refresh_jitter=self._refresh_jitter,
            metrics_interval=self._metrics_interval,
            metrics_jitter=self._metrics_jitter,
            disable_metrics=self._disable_metrics,
            disable_registration=self._disable_registration,
            custom_options=self._custom_options,
            custom_strategies=self._custom_strategies,
            cache_directory=self._cache_directory,
            project_name=self._project_name,
            verbose_log_level=self._verbose_log_level,
            cache=self._cache,
            # https://apscheduler.readthedocs.io/en/3.x/userguide.html#choosing-the-right-scheduler-job-store-s-executor-s-and-trigger-s
            # Using the default scheduler provided by Unleash, you'll only execute the jobs when a request is made
            # I haven't been able to make it work, though
            # scheduler=GeventScheduler(),
            # scheduler_executor=f"unleash_executor_{uuid4()}",
        )

        if self._fake_initialize:
            unleash_client.is_initialized = True
        else:
            unleash_client.initialize_client()

        return unleash_client


class FeatureManagementMiddleware:
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
        user_context = {
            "userId": user_id,
            "browser": browser,
        }
        cnpj = request.session.get("cnpj")
        if cnpj:
            user_context["cnpj"] = cnpj
        # https://docs.getunleash.io/unleash-client-python/usage.html
        client = retrieve_client()
        client.unleash_static_context = client.unleash_static_context | user_context

    def _after_calling_view(self, request):
        pass


# https://docs.getunleash.io/unleash-client-python/usage.html
_client = Client().connect()


def retrieve_client() -> UnleashClient:
    return _client
