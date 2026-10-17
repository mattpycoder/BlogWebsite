import logging
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import Page, sync_playwright

from app.autotests.config.application_settings import application_settings
from app.autotests.context import context
from app.autotests.utils.browser import create_browser
from app.autotests.utils.config import BrowserConfig, BrowserType, ContextConfig
from app.autotests.utils.config_parser import PYPROJECT_CONFIG_FILE, parse_config_file
from app.autotests.utils.context import create_context

logger = logging.getLogger(__name__)


def pytest_configure(config: Any) -> None:
    config_file = Path(config.rootdir, PYPROJECT_CONFIG_FILE)
    settings_selection = parse_config_file(config_file)
    application_settings.headless = settings_selection.get("headless_mode", True)
    application_settings.debug_locally = settings_selection.get("debug_locally", False)
    if application_settings.debug_locally:
        application_settings.headless = False


@pytest.fixture(scope="session", autouse=True)
def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )


@pytest.fixture(autouse=True)
def page() -> Generator[Page]:
    with sync_playwright() as p:
        logger.info("Initializing browser and context...")
        browser_config = BrowserConfig(
            browser=BrowserType.CHROMIUM,
            headless=application_settings.headless,
        )
        browser = create_browser(p, browser_config)
        context_config = ContextConfig()
        browser_context = create_context(browser, context_config)
        test_page = browser_context.new_page()

        context.set_page(test_page)

        yield test_page

        browser_context.close()
        browser.close()
