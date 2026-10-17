from dataclasses import dataclass
from enum import StrEnum


class BrowserType(StrEnum):
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


@dataclass(frozen=True)
class BrowserConfig:
    browser: BrowserType = BrowserType.CHROMIUM
    headless: bool = True
    slow_mo: int = 0


@dataclass(frozen=True)
class ContextConfig:
    viewport_width: int = 1366
    viewport_height: int = 768
    locale: str = "en-US"
    timezone_id: str | None = None
    ignore_https_errors: bool = False
    accept_downloads: bool = True
