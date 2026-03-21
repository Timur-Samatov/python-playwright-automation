import allure
from pages import *


def test_left_navigation_panel(page, base_url, fresh_registered_user):
    """Test viewing account details for a specific account."""

    home_page = HomePage(page, base_url)
    open_account_page = OpenAccountPage(page, base_url)
    overview_page = OverviewPage(page, base_url)
    transfer_page = TransferPage(page, base_url)
    bill_payment_page = BillPayPage(page, base_url)
    find_transactions_page = FindTransactionsPage(page, base_url)
    update_profile_page = UpdateProfilePage(page, base_url)
    request_loan_page = RequestLoanPage(page, base_url)

    with allure.step("Login"):
        home_page.login(
            fresh_registered_user["username"], fresh_registered_user["password"]
        )

    with allure.step("Navigate to Home Page and validate URL"):
        home_page.goto()
        home_page.validate_url()

    with allure.step("Validate Left Navigation Panel links are visible from Home Page"):
        home_page.validate_navigation_links()

    with allure.step("Click on 'Open New Account' link from Left Navigation Panel"):
        home_page.open_new_account_link.click()

    with allure.step(
        "Validate Open New Account Page URL and Left Navigation Panel links"
    ):
        open_account_page.validate_url()
        open_account_page.validate_navigation_links()

    with allure.step("Click on 'Accounts Overview' link from Left Navigation Panel"):
        open_account_page.accounts_overview_link.click()

    with allure.step(
        "Validate Accounts Overview Page URL and Left Navigation Panel links"
    ):
        overview_page.validate_url()
        overview_page.validate_navigation_links()

    with allure.step("Click on 'Transfer Funds' link from Left Navigation Panel"):
        overview_page.transfer_funds_link.click()

    with allure.step(
        "Validate Transfer Funds Page URL and Left Navigation Panel links"
    ):
        transfer_page.validate_url()
        transfer_page.validate_navigation_links()

    with allure.step("Click on 'Bill Pay' link from Left Navigation Panel"):
        transfer_page.bill_pay_link.click()

    with allure.step("Validate Bill Pay Page URL and Left Navigation Panel links"):
        bill_payment_page.validate_url()
        bill_payment_page.validate_navigation_links()

    with allure.step("Click on 'Find Transactions' link from Left Navigation Panel"):
        bill_payment_page.find_transactions_link.click()

    with allure.step(
        "Validate 'Find Transactions' URL and Left Navigation Panel links"
    ):
        find_transactions_page.validate_url()
        find_transactions_page.validate_navigation_links()

    with allure.step("Click on 'Update Contact Info' link from Left Navigation Panel"):
        find_transactions_page.update_contact_info_link.click()

    with allure.step(
        "Validate 'Update Profile' Page URL and Left Navigation Panel links"
    ):
        update_profile_page.validate_url()
        update_profile_page.validate_navigation_links()

    with allure.step("Click on 'Request Loan' link from Left Navigation Panel"):
        update_profile_page.request_loan_link.click()

    with allure.step(
        "Validate 'Request Loan' Page URL and Left Navigation Panel links"
    ):
        request_loan_page.validate_url()
        request_loan_page.validate_navigation_links()
