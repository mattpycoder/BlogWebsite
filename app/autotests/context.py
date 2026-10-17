from playwright.sync_api import Page


class TestContext:
    def __init__(self) -> None:
        self._page: Page | None = None

    def set_page(self, page: Page) -> None:
        self._page = page

    def get_page(self) -> Page:
        if self._page is None:
            raise RuntimeError("Playwright page has not been initialized")
        return self._page

    def clear_page(self) -> None:
        self._page = None


context = TestContext()
