import re

from time import sleep


def wait_for_message_in_log(caplog, message_to_wait, message_count_to_wait=1, max_seconds_to_wait=5):
    """
    Awaits for a message that must appears for a given number of times.
    Args:
        caplog: An instance of LogCaptureFixture from pytest that is used to retrieve a list of format-interpolated log messages.
            Refer to: https://docs.pytest.org/en/latest/reference.html#_pytest.logging.LogCaptureFixture
        message_to_wait: A regex that'll be used to match a message in the logs.
        message_count_to_wait: Optionally integer parameter that indicates how many `message_to_wait` we
            need to find in the logs. Defaults to 1.
        max_seconds_to_wait: Optionally integer parameter that indicates how many seconds the search will
            awaits for the messages appears in the logs. Defaults to 5 seconds
    """
    regex = re.compile(message_to_wait)

    while max_seconds_to_wait:
        message_in_logs_count_iterator = filter(lambda message: regex.match(message), caplog.messages)
        message_in_logs_count = sum(1 for _ in message_in_logs_count_iterator)
        if message_in_logs_count == message_count_to_wait:
            return
        max_seconds_to_wait -= 1
        sleep(1)

    raise MessageNotFoundException


class MessageNotFoundException(Exception):
    pass
