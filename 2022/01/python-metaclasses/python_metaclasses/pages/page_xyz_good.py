from python_metaclasses.decorators import take_screenshot


class BasePageMetaClass(type):
    def __new__(cls, subclass_name, bases, dictionary):
        for attribute in dictionary:
            value = dictionary[attribute]
            should_be_decorated_with_screenshot = attribute.startswith("step_") and callable(value)
            if should_be_decorated_with_screenshot:
                dictionary[attribute] = take_screenshot(value)
        return type.__new__(cls, subclass_name, bases, dictionary)


class MyPageXYZSampleGood(object, metaclass=BasePageMetaClass):
    def step_access_home_page(self):
        pass

    def step_access_ticker_panel(self):
        pass

    def step_select_ticker(self, ticker_name: str):
        pass

    def step_access_my_profile(self):
        pass

    def do_not_take_screenshot(self):
        pass
