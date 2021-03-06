from contextlib import suppress

from selenium.webdriver.common.by import By

from tests import settings
from tests.cognito_user_pool import UsernameExistsException
from tests.cognito_user_pool import UserToBeRegistered
from tests.helpers import BaseTestCase
from tests.pages.cognito_hosted_ui import CognitoHostedUI
from tests.pages.product import ProductApp
from tests.settings import retrieve_browser


class ProductATestCase(BaseTestCase):
    def setUp(self):
        self.window_details = retrieve_browser(enable_virtual_display=settings.ENABLE_VIRTUAL_DISPLAY)
        self.product_a = ProductApp(self.window_details.browser, settings.PRODUCT_A_URL)
        self.cognito_hosted_ui = CognitoHostedUI(self.window_details.browser)

    def test_should_login_user_using_authorization_code_grant_type(self):
        # Arrange
        user = UserToBeRegistered("jafar@agrabah.com", "Sorcerer Jafar", "you-are-late")
        with suppress(UsernameExistsException):
            self.cognito_user_pool.create_user(user)
        self.cognito_user_pool.confirm_user_as_admin(user.email)
        # Act
        self.product_a.access_landing_page()
        self.product_a.initiate_login_flow()
        self.cognito_hosted_ui.authenticate(user.email, user.password)
        # Assert
        locator = (By.XPATH, f"//*[contains(@data-testid,'user-email-output')]")
        element = self.wait_until_visible(locator)
        assert element.text == f"Your e-mail is {user.email}!"
        assert self.retrieve_cookie("product_a_sessionid")
        current_url = self.retrieve_current_url()
        assert current_url.startswith(self.product_a.address)

    def tearDown(self):
        self.window_details.close_gracefully()
