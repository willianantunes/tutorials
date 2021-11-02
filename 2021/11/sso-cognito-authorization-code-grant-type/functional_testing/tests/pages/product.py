from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from tests.pages.abstract_page import BasePageMetaClass


class ProductApp(object, metaclass=BasePageMetaClass):
    def __init__(self, driver: WebDriver, address):
        self.driver = driver
        self.address = address

    def initiate_login_flow(self):
        login_link_test_id = "login-link"
        element = self.driver.find_element(By.XPATH, f"//*[contains(@data-testid,'{login_link_test_id}')]")
        element.click()

    def access_landing_page(self):
        self.driver.get(self.address)
