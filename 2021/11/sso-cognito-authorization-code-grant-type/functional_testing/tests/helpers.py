import unittest

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
