import logging
import time
import unittest

from unittest import mock

from python_metaclasses.decorators import measure_it
from python_metaclasses.decorators import take_screenshot

logger = logging.getLogger(__name__)


class MyPageSampleBad:
    def show_my_profile(self):
        start = time.perf_counter()
        try:
            # Main logic
            for i in range(1, 100):
                pass
            # End of main logic
        finally:
            elapsed = time.perf_counter() - start
            logger.info(f"show_my_profile took {elapsed:0.2f} seconds")


class MyPageSampleOK:
    @measure_it
    def show_my_profile(self):
        for i in range(1, 100):
            pass


class MyPageXYZSampleBad:
    @take_screenshot
    def step_access_home_page(self):
        pass

    @take_screenshot
    def step_access_ticker_panel(self):
        pass

    @take_screenshot
    def step_select_ticker(self, ticker_name: str):
        pass

    @take_screenshot
    def step_acess_my_profile(self):
        pass


class MeasureItTests(unittest.TestCase):
    @mock.patch("python_metaclasses.decorators.logger")
    def test_should_log_information_about_time_execution(self, mocked_logger):
        # Arrange
        my_page_sample_instance = MyPageSampleOK()
        # Act
        my_page_sample_instance.show_my_profile()
        # Assert
        mocked_info = mocked_logger.info
        mocked_info.assert_called_once()
        received_message = mocked_logger.info.call_args[0][0]
        expected_message_regex = r"^show_my_profile from test_decorators with args \(.+\) took [0-9]\.[0-9]{2} seconds$"
        self.assertRegex(received_message, expected_message_regex)
