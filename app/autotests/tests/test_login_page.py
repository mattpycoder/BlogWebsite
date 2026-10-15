import allure
import pytest

from app.autotests import steps


class TestLoginPage:
    @pytest.mark.standalone
    @pytest.mark.priority_0
    def test_verify_login_to_user_profile(self):
        with allure.step("1"):
            steps.open_blog_website.open_blog_website_in_standalone()
            steps.login.open_login_page()
            steps.login.login_to_profile()
        with allure.step("2"):
            steps.user_profile.wait_user_profile_name_to_be_visible()
