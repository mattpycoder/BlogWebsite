import logging
import os

import allure

from app.autotests import steps
from app.autotests.context import context
from app.autotests.steps.base_steps import BaseSteps

logger = logging.getLogger(__name__)


class OpenBlogWebsiteSteps(BaseSteps):
    @allure.step("Open Blog Website in standalone")
    def open_blog_website_in_standalone(self):
        base_url = os.getenv("BASE_URL", "http://127.0.0.1:5000")
        logger.info(f"Open Blog Website in standalone. URL: {base_url}")
        context.get_page().goto(base_url)
        steps.base_steps.base_page.start_writing_button.wait_for(state="visible")


open_blog_website = OpenBlogWebsiteSteps()
