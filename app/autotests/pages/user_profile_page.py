from playwright.sync_api import Locator, Page

from app.autotests.context import context
from app.autotests.pages.base_page import BasePage


class UserProfilePage(BasePage):
    @property
    def page(self) -> Page:
        return context.get_page()

    @property
    def user_profile_name(self) -> Locator:
        return self.page.locator('[data-qa-name="user-profile-name"]')
