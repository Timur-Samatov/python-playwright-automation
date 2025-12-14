from pages.base_page import BasePage


class OverviewPage(BasePage):
    """Page Object Model for the Account Overview page."""

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        # Locators
        self.account_list = self.page.locator("#accountTable")
        self.account_links = self.page.locator("#accountTable a")

    def goto(self):
        self.page.goto(f"{self.base_url}/parabank/overview.htm")
