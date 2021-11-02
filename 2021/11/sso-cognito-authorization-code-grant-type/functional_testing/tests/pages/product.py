from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from tests import settings
from tests.helpers import take_screenshot


class ProductApp:
    def __init__(self, driver: WebDriver, address):
        self.driver = driver
        self.address = address

    @take_screenshot(settings.SELENIUM_TAKE_SCREENSHOT)
    def initiate_login_flow(self):
        login_link_test_id = "login-link"
        element = self.driver.find_element(By.XPATH, f"//*[contains(@data-testid,'{login_link_test_id}')]")
        element.click()

    @take_screenshot(settings.SELENIUM_TAKE_SCREENSHOT)
    def access_landing_page(self):
        self.driver.get(self.address)
