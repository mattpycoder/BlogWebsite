import logging

from app.autotests.pages.user_profile_page import UserProfilePage
from app.autotests.steps.base_steps import BaseSteps

logger = logging.getLogger(__name__)


class UserProfileSteps(BaseSteps):
    @property
    def user_profile_page(self) -> UserProfilePage:
        return UserProfilePage()

    def wait_user_profile_name_to_be_visible(self):
        logger.info("Wait user profile page is visible")
        self.user_profile_page.user_profile_name.wait_for(state="visible")


user_profile = UserProfileSteps()
