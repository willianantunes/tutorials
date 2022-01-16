import unittest

from unittest import mock

from python_metaclasses.decorators import FailedToTakeScreenshotException
from python_metaclasses.pages.page_xyz_good import MyPageXYZSampleGood


class MyPageXYZSampleGoodTests(unittest.TestCase):
    @mock.patch("python_metaclasses.decorators.logger")
    def test_should_take_screenshots_when_required(self, mocked_logger):
        # Arrange
        my_page_sample_instance = MyPageXYZSampleGood()
        # Act
        my_page_sample_instance.step_access_home_page()
        my_page_sample_instance.step_access_ticker_panel()
        my_page_sample_instance.step_select_ticker("cogn3")
        my_page_sample_instance.step_access_my_profile()
        my_page_sample_instance.do_not_take_screenshot()
        # Assert
        mocked_info = mocked_logger.info
        self.assertEqual(4, mocked_info.call_count)
        messages = []
        for call_arg in mocked_logger.info.call_args_list:
            first_argument = call_arg[0][0]
            messages.append(first_argument)
        expected_messages = [
            "Screenshot has been taken for step_access_home_page",
            "Screenshot has been taken for step_access_ticker_panel",
            "Screenshot has been taken for step_select_ticker",
            "Screenshot has been taken for step_access_my_profile",
        ]
        self.assertEqual(expected_messages, messages)

    @mock.patch("python_metaclasses.decorators.logger")
    def test_should_raise_exception_given_take_screenshot_fails(self, mocked_logger):
        # Arrange
        mocked_info = mocked_logger.info
        mocked_info.side_effect = [None, Exception]
        my_page_sample_instance = MyPageXYZSampleGood()
        # Act and assert
        with self.assertRaises(FailedToTakeScreenshotException):
            my_page_sample_instance.step_access_home_page()
            my_page_sample_instance.step_access_my_profile()
        self.assertEqual(2, mocked_info.call_count)
