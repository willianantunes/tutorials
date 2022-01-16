from python_metaclasses.decorators import take_screenshot


class MyPageXYZSampleBad:
    @take_screenshot
    def step_access_home_page(self):
        pass

    @take_screenshot
    def step_access_ticker_panel(self):
        pass

    @take_screenshot
    def step_select_ticker(self, ticker_name: str):
        pass

    @take_screenshot
    def step_access_my_profile(self):
        pass

    def do_not_take_screenshot(self):
        pass
