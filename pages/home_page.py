from pages.base_page import BasePage
from pages.components.customer_login import CustomerLogin


class HomePage(BasePage):
    """Page Object Model for Parabank Home (index) page."""

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self.customer_login = CustomerLogin(page)
        # Locators
        self.welcome_message = self.page.locator("#leftPanel .smallText")
        self.error_message = self.page.locator(".error")

    def goto(self):
        self.page.goto(f"{self.base_url}/parabank/index.htm")

    def login(self, username, password):
        self.goto()
        self.customer_login.login(username, password)
