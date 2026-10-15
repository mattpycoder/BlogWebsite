import logging

import allure

from app.autotests import steps
from app.autotests.consts import User
from app.autotests.pages.login_page import LoginPage
from app.autotests.steps.base_steps import BaseSteps

logger = logging.getLogger(__name__)


class LoginSteps(BaseSteps):
    @property
    def login_page(self) -> LoginPage:
        return LoginPage()

    @allure.step("Navigate to Login page")
    def open_login_page(self) -> None:
        logger.info("Navigating to Login page")
        steps.base_steps.base_page.login_button.click()
        self.login_page.username_field.wait_for(state="visible")
        self.login_page.password_field.wait_for(state="visible")
        self.login_page.remember_me_checkbox.wait_for(state="visible")
        self.login_page.sign_in_button.wait_for(state="visible")

    @allure.step("Login to user profile page")
    def login_to_profile(self) -> None:
        logger.info("Login to user profile page")
        self.open_login_page()
        self.login_page.username_field.fill(User.USERNAME)
        self.login_page.password_field.fill(User.PASSWORD)
        self.login_page.sign_in_button.click()


login = LoginSteps()
