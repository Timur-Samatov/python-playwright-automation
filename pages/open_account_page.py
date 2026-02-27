from pages.base_page import BasePage
from pages.components.left_navigation_panel import LeftNavigationPanel


class OpenAccountPage(BasePage, LeftNavigationPanel):
    """Page Object Model for Open New Account page."""

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        LeftNavigationPanel.__init__(self, page)
        self.page_url = f"{self.base_url}/parabank/openaccount.htm"
