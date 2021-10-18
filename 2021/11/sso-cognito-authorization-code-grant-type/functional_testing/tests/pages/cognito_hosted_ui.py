from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class CognitoHostedUI:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def authenticate(self, email, password):
        username_input = self.driver.find_element(By.ID, "signInFormUsername")
        username_input.send_keys(email)
        password_input = self.driver.find_element(By.ID, "signInFormPassword")
        password_input.send_keys(password)
        submit_button = None
        buttons = self.driver.find_elements(By.XPATH, "//input[@name='signInSubmitButton']")
        for button in buttons:
            if button.is_displayed():
                submit_button = button
        submit_button.click()
