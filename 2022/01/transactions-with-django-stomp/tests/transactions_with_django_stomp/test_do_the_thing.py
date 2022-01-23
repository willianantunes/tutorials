import logging

from uuid import uuid4

from django.utils import timezone
from django_stomp.execution import start_processing

from tests.support.caplog_helper import wait_for_message_in_log
from tests.support.django_stomp_helpers import get_latest_message_from_destination_using_test_listener
from tests.support.django_stomp_helpers import publish_to_destination
from tests.transactions_with_django_stomp.change_callback_do_the_thing import callback_scenario_1
from tests.transactions_with_django_stomp.change_callback_do_the_thing import callback_scenario_2
from tests.transactions_with_django_stomp.change_callback_do_the_thing import callback_scenario_3

xyz_destination = "/queue/xyz"
acme_destination = "/queue/acme"


def test_should_publish_events_in_two_queues_scenario_1(caplog):
    # Arrange
    caplog.set_level(logging.DEBUG)
    some_destination = f"scenario-1-{uuid4()}"
    sample_body = {
        "owner_id": uuid4(),
        "title": "All right, so I'm back in high school, standing in the middle of the cafeteria",
        "salt_addicted": True,
        "registered_at": timezone.now(),
    }
    publish_to_destination(some_destination, sample_body)
    # Act
    custom_uuid_for_destination = uuid4()
    extra_options = {"is_testing": True, "return_listener": True, "param_to_callback": custom_uuid_for_destination}
    message_consumer = start_processing(some_destination, callback_scenario_1, **extra_options)
    wait_for_message_in_log(caplog, r"All the events have been sent")
    message_consumer.close()
    # Assert
    final_xyz_destination = f"{xyz_destination}-scenario-1-{custom_uuid_for_destination}"
    final_acme_destination = f"{acme_destination}-scenario-1-{custom_uuid_for_destination}"
    message_from_xyz = get_latest_message_from_destination_using_test_listener(final_xyz_destination)
    message_from_acme = get_latest_message_from_destination_using_test_listener(final_acme_destination)
    assert message_from_xyz.body == {
        "who_did_the_thing_id": str(sample_body["owner_id"]),
        "title": sample_body["title"],
    }
    assert message_from_acme.body == {
        "who_did_the_thing_id": str(sample_body["owner_id"]),
        "is_salt_addicted": sample_body["salt_addicted"],
        "registered_at": sample_body["registered_at"].isoformat(timespec="milliseconds"),
    }


def test_should_send_message_to_dlq_scenario_2(caplog):
    # Arrange
    caplog.set_level(logging.DEBUG)
    some_destination = f"scenario-2-{uuid4()}"
    sample_body = {
        "owner_id": uuid4(),
        "title": "You're feeling a lot of pain right now. You're angry. You're hurting. Can' I tell you what the answer is?",
        "salt_addicted": True,
        "registered_at": timezone.now(),
    }
    publish_to_destination(some_destination, sample_body)
    # Act
    custom_uuid_for_destination = uuid4()
    extra_options = {"is_testing": True, "return_listener": True, "param_to_callback": custom_uuid_for_destination}
    message_consumer = start_processing(some_destination, callback_scenario_2, **extra_options)
    wait_for_message_in_log(caplog, r"Trying to do NACK explicitly sending the message to DLQ.*")
    message_consumer.close()
    # Assert
    some_destination_dlq = f"/queue/DLQ.{some_destination}"
    message_from_dlq = get_latest_message_from_destination_using_test_listener(some_destination_dlq)
    assert message_from_dlq.body == {
        "owner_id": str(sample_body["owner_id"]),
        "title": sample_body["title"],
        "salt_addicted": sample_body["salt_addicted"],
        "registered_at": sample_body["registered_at"].isoformat(timespec="milliseconds"),
    }


def test_should_send_message_to_dlq_scenario_3(caplog):
    # Arrange
    caplog.set_level(logging.DEBUG)
    some_destination = f"scenario-3-{uuid4()}"
    sample_body = {
        "owner_id": uuid4(),
        "title": "I don't want to be single, OK?! I just... I just wanna be married again!",
        "salt_addicted": False,
        "registered_at": timezone.now(),
    }
    publish_to_destination(some_destination, sample_body)
    # Act
    extra_options = {"is_testing": True, "return_listener": True}
    message_consumer = start_processing(some_destination, callback_scenario_3, **extra_options)
    wait_for_message_in_log(caplog, r"Trying to do NACK explicitly sending the message to DLQ.*")
    message_consumer.close()
    # Assert
    some_destination_dlq = f"/queue/DLQ.{some_destination}"
    message_from_dlq = get_latest_message_from_destination_using_test_listener(some_destination_dlq)
    assert message_from_dlq.body == {
        "owner_id": str(sample_body["owner_id"]),
        "title": sample_body["title"],
        "salt_addicted": sample_body["salt_addicted"],
        "registered_at": sample_body["registered_at"].isoformat(timespec="milliseconds"),
    }
