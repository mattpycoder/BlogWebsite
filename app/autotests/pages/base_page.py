from playwright.sync_api import Locator, Page

from app.autotests.context import context


class BasePage:
    @property
    def page(self) -> Page:
        return context.get_page()

    @property
    def start_writing_button(self) -> Locator:
        return self.page.locator('[data-qa-name="start-writing-button"]')

    @property
    def login_button(self) -> Locator:
        return self.page.locator('[data-qa-name="login-button"]')

    @property
    def remember_me_checkbox(self) -> Locator:
        return self.page.locator('[data-qa-name="remember-me-checkbox"]')
