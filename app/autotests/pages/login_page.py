from playwright.sync_api import Locator, Page

from app.autotests.context import context
from app.autotests.pages.base_page import BasePage


class LoginPage(BasePage):
    @property
    def page(self) -> Page:
        return context.get_page()

    @property
    def username_field(self) -> Locator:
        return self.page.locator('[data-qa-name="username-field"]')

    @property
    def password_field(self) -> Locator:
        return self.page.locator('[data-qa-name="password-field"]')

    @property
    def sign_in_button(self) -> Locator:
        return self.page.locator('[data-qa-name="sign-in-button"]')
