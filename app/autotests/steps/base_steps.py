from app.autotests.pages.base_page import BasePage


class BaseSteps:
    @property
    def base_page(self) -> BasePage:
        return BasePage()


base_steps = BaseSteps()
