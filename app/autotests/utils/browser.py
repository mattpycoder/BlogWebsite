from playwright.sync_api import Browser, Playwright

from .config import BrowserConfig


def create_browser(
    playwright: Playwright,
    config: BrowserConfig,
) -> Browser:
    browser_type = getattr(playwright, config.browser.value)

    return browser_type.launch(
        headless=config.headless,
        slow_mo=config.slow_mo,
    )
