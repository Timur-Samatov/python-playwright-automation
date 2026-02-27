from pages.base_page import BasePage
from pages.components.left_navigation_panel import LeftNavigationPanel


class TransferPage(BasePage, LeftNavigationPanel):
    """Page Object Model for the Transfer Funds page."""

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        LeftNavigationPanel.__init__(self, page)
        self.page_url = f"{self.base_url}/parabank/transfer.htm"
        # Locators
        self.amount_input = self.page.locator("#amount")
        self.from_account_select = self.page.locator("#fromAccountId")
        self.to_account_select = self.page.locator("#toAccountId")
        self.transfer_button = self.page.locator("input[value='Transfer']")
        self.result_message = self.page.locator("#showResult")

    def transfer_funds(self, amount, from_account_id, to_account_id):
        self.amount_input.fill(str(amount))
        self.from_account_select.select_option(str(from_account_id))
        self.to_account_select.select_option(str(to_account_id))
        self.transfer_button.click()
