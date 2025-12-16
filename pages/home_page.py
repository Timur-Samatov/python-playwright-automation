from pages.base_page import BasePage
from pages.components.customer_login import CustomerLogin
from pages.components.left_navigation_panel import LeftNavigationPanel


class HomePage(BasePage, LeftNavigationPanel):
    """Page Object Model for Parabank Home (index) page."""

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        LeftNavigationPanel.__init__(self, page)
        self.customer_login = CustomerLogin(page)
        self.page_url = f"{self.base_url}/parabank/index.htm"
        # Locators
        self.welcome_message = self.page.locator("#leftPanel .smallText")
        self.error_message = self.page.locator(".error")

    def login(self, username, password):
        self.goto()
        self.customer_login.login(username, password)
