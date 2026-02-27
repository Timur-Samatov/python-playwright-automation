from pages.base_page import BasePage
from pages.components.left_navigation_panel import LeftNavigationPanel


class OverviewPage(BasePage, LeftNavigationPanel):
    """Page Object Model for the Account Overview page."""

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        LeftNavigationPanel.__init__(self, page)
        self.page_url = f"{self.base_url}/parabank/overview.htm"
        # Locators
        self.account_list = self.page.locator("#accountTable")
        self.account_links = self.page.locator("#accountTable a")
