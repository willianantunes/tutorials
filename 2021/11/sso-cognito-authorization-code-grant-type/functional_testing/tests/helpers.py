import unittest

from datetime import datetime
from functools import wraps
from typing import Optional
from typing import Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.cognito_user_pool import CognitoUserPool


class BaseTestCase(unittest.TestCase):
    cognito_user_pool: CognitoUserPool

    @classmethod
    def setUpClass(cls) -> None:
        cls.cognito_user_pool = CognitoUserPool()

    @classmethod
    def tearDownClass(cls) -> None:
        users, _ = cls.cognito_user_pool.list_users()
        for user in users:
            cls.cognito_user_pool.delete_user(user.username)

    def wait_until_visible(self, locator: Tuple[By, str]):
        wait = WebDriverWait(self.window_details.browser, 10)
        return wait.until(EC.visibility_of_element_located(locator))

    def retrieve_current_url(self) -> str:
        return self.window_details.browser.current_url

    def retrieve_cookie(self, name) -> Optional[dict]:
        all_cookies = self.window_details.browser.get_cookies()
        for cookie in all_cookies:
            if cookie["name"] == name:
                return cookie
        return None


def take_screenshot(enable=True):
    def main_wrapper(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            finally:
                if enable:
                    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
                    file_name = f"{timestamp}-{func.__name__}.png"
                    image_as_binary_data = self.driver.get_screenshot_as_png()
                    with open(file_name, "wb") as file_image:
                        file_image.write(image_as_binary_data)

        return wrapped

    return main_wrapper
