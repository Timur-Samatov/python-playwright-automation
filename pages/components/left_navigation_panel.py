from playwright.sync_api import expect


class LeftNavigationPanel:
    """Page Object Model for the Left Navigation Panel component."""

    def __init__(self, page):
        self.page = page
        # Locators
        self.open_new_account_link = self.page.locator("#leftPanel").get_by_role(
            "link", name="Open New Account"
        )
        self.accounts_overview_link = self.page.locator(
            "//a[text()='Accounts Overview']"
        )
        self.transfer_funds_link = self.page.locator("#leftPanel").get_by_role(
            "link", name="Transfer Funds"
        )
        self.bill_pay_link = self.page.locator("#leftPanel").get_by_role(
            "link", name="Bill Pay"
        )
        self.find_transactions_link = self.page.locator("#leftPanel").get_by_role(
            "link", name="Find Transactions"
        )
        self.update_contact_info_link = self.page.locator("#leftPanel").get_by_role(
            "link", name="Update Contact Info"
        )
        self.request_loan_link = self.page.locator("#leftPanel").get_by_role(
            "link", name="Request Loan"
        )
        self.logout_link = self.page.locator("#leftPanel").get_by_role(
            "link", name="Log Out"
        )

    def validate_navigation_links(self):
        """Validate that all navigation links are visible."""
        expect(self.open_new_account_link).to_be_visible()
        expect(self.accounts_overview_link).to_be_visible()
        expect(self.transfer_funds_link).to_be_visible()
        expect(self.bill_pay_link).to_be_visible()
        expect(self.find_transactions_link).to_be_visible()
        expect(self.update_contact_info_link).to_be_visible()
        expect(self.request_loan_link).to_be_visible()
        expect(self.logout_link).to_be_visible()
