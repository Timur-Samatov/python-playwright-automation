from pages.base_page import BasePage


class ActivityPage(BasePage):
    """Page Object Model for the Activity (account) page."""

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        # Locators
        self.account_number_label = self.page.get_by_text("Account Number:")
        self.account_number_value = self.page.locator("#accountId")
        self.balance_label = self.page.get_by_text("Balance:")
        self.balance_value = self.page.locator("#balance")
        self.account_type_label = self.page.get_by_text("Account Type:")
        self.account_type_value = self.page.locator("#accountType")
        self.transactions_table = self.page.locator("#transactionTable")

    def goto(self, account_id):
        self.page.goto(f"{self.base_url}/parabank/activity.htm?id={account_id}")
