from unittest import mock

from django_stomp.helpers import create_dlq_destination_from_another_destination
from django_stomp.services import producer

from transactions_with_django_stomp import do_the_thing
from transactions_with_django_stomp.do_the_thing import build_news_and_dispatch_them

callback_scenario_1 = (
    "tests.transactions_with_django_stomp.change_callback_do_the_thing.build_news_and_dispatch_them_mocked"
)
callback_scenario_2 = "tests.transactions_with_django_stomp.change_callback_do_the_thing.build_news_and_dispatch_them_mocked_raise_exception_during_second_send"
callback_scenario_3 = "tests.transactions_with_django_stomp.change_callback_do_the_thing.build_news_and_dispatch_them_mocked_raise_exception_during_computation"


def build_news_and_dispatch_them_mocked(payload, append_to_destination):
    # Change destinations so we can retrieve them during tests
    with mock.patch.object(do_the_thing, "xyz_destination", f"/queue/xyz-scenario-1-{append_to_destination}"):
        with mock.patch.object(do_the_thing, "acme_destination", f"/queue/acme-scenario-1-{append_to_destination}"):
            # Let's call our main callback function!
            build_news_and_dispatch_them(payload)


def build_news_and_dispatch_them_mocked_raise_exception_during_second_send(payload, append_to_destination):
    with mock.patch.object(do_the_thing, "xyz_destination", f"/queue/xyz-scenario-2-{append_to_destination}"):
        with mock.patch.object(do_the_thing, "acme_destination", f"/queue/acme-scenario-2-{append_to_destination}"):
            with mock.patch.object(
                producer,
                "create_dlq_destination_from_another_destination",
                wraps=create_dlq_destination_from_another_destination,
            ) as mocked_create_dlq_destination_from_another_destination:
                # This side effect configuration will make "send function" work only once
                mocked_create_dlq_destination_from_another_destination.side_effect = [
                    create_dlq_destination_from_another_destination,
                    RuntimeError,
                ]
                build_news_and_dispatch_them(payload)


def build_news_and_dispatch_them_mocked_raise_exception_during_computation(payload):
    with mock.patch(
        "transactions_with_django_stomp.do_the_thing.retrieve_events_to_be_dispatched"
    ) as mocked_retrieve_events_to_be_dispatched:
        mocked_retrieve_events_to_be_dispatched.side_effect = [RuntimeError]
        build_news_and_dispatch_them(payload)
