from tests import settings
from tests.helpers import take_screenshot


class BasePageMetaClass(type):
    def __new__(cls, subclass_name, bases, dictionary):
        for attribute in dictionary:
            value = dictionary[attribute]
            if not attribute.startswith("__") and callable(value):
                setup = settings.SELENIUM_TAKE_SCREENSHOT, settings.SELENIUM_SCREENSHOTS_FOLDER
                dictionary[attribute] = take_screenshot(*setup)(value)
        return type.__new__(cls, subclass_name, bases, dictionary)
