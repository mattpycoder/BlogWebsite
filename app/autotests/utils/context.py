from playwright.sync_api import Browser, BrowserContext

from .config import ContextConfig


def create_context(
    browser: Browser,
    config: ContextConfig,
) -> BrowserContext:
    return browser.new_context(
        viewport={
            "width": config.viewport_width,
            "height": config.viewport_height,
        },
        locale=config.locale,
        timezone_id=config.timezone_id,
        ignore_https_errors=config.ignore_https_errors,
        accept_downloads=config.accept_downloads,
    )
