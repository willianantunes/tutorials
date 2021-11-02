import os
import pathlib

from dataclasses import dataclass
from distutils.util import strtobool
from typing import Optional

import webdriver_manager

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

#####
# Project properties

# Interesting links to look at:
# https://gist.github.com/rothnic/79e036ce4564a3ecb2708e248d163ceb
# https://github.com/golemhq/webdriver-manager/tree/0e72ef1e4c882989fd78cd50b9e46a4503e5fac5#using-webdriver-manager-from-code
# https://selenium-python.readthedocs.io/getting-started.html#simple-usage

CHROME_VERSION = os.getenv("CHROME_VERSION", "92.0.4515.107")
DOWNLOAD_CHROME = bool(strtobool(os.getenv("DOWNLOAD_CHROME", "True")))
PRODUCT_A_URL = os.getenv("PRODUCT_A_URL", "http://localhost:8000")
PRODUCT_B_URL = os.getenv("PRODUCT_A_URL", "http://localhost:8001")
ENABLE_VIRTUAL_DISPLAY = bool(strtobool(os.getenv("ENABLE_VIRTUAL_DISPLAY", "False")))
SELENIUM_IMPLICIT_WAIT = int(os.getenv("SELENIUM_IMPLICIT_WAIT", 0))
SELENIUM_TAKE_SCREENSHOT = bool(strtobool(os.getenv("SELENIUM_TAKE_SCREENSHOT", "False")))
SELENIUM_SCREENSHOTS_FOLDER = os.getenv("SELENIUM_SCREENSHOTS_FOLDER", "../screenshots")

AWS_COGNITO_USER_POOL_ID = "AWS_COGNITO_USER_POOL_ID"
AWS_COGNITO_REGION = AWS_COGNITO_USER_POOL_ID.split("_")[0]
AWS_COGNITO_SERVICE_ACCOUNT_ACCESS_KEY = "AWS_COGNITO_SERVICE_ACCOUNT_ACCESS_KEY"
AWS_COGNITO_SERVICE_ACCOUNT_ACCESS_SECRET = "AWS_COGNITO_SERVICE_ACCOUNT_ACCESS_SECRET"
AWS_COGNITO_APP_CLIENT_ID = "AWS_COGNITO_APP_CLIENT_ID"
AWS_COGNITO_APP_CLIENT_SECRET = "AWS_COGNITO_APP_CLIENT_SECRET"


#####
# Helpful things


@dataclass(frozen=True)
class WindowDetails:
    display: Optional[Display]
    browser: WebDriver

    def close_gracefully(self):
        self.browser.quit()
        if self.display:
            self.display.stop()


def retrieve_browser(width=800, height=600, enable_virtual_display=True):
    display = None
    driver_output_folder = "./tmp"

    if enable_virtual_display:
        display = Display(visible=False)
        display.start()

    chromedriver_executable_path_as_str = "chromedriver"
    if DOWNLOAD_CHROME:
        webdriver_manager.update("chrome", driver_output_folder, version=CHROME_VERSION)
        chromedriver_executable_path = list(pathlib.Path(driver_output_folder).glob("chromedriver*"))[0]
        chromedriver_executable_path_as_str = str(chromedriver_executable_path.absolute())

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("prefs", {"download.prompt_for_download": False})

    browser = webdriver.Chrome(executable_path=chromedriver_executable_path_as_str, options=chrome_options)
    browser.set_window_size(width, height)
    browser.implicitly_wait(SELENIUM_IMPLICIT_WAIT)

    return WindowDetails(display, browser)
