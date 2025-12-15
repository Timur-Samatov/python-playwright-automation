import allure
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.overview_page import OverviewPage
from pages.activity_page import ActivityPage
from src.clients.parabank_api_client import ParaBankAPIClient
from src.enums.account_types import AccountType


def test_view_account_details(page, base_url, user_1):
    """Test viewing account details for a specific account."""

    # API Setup: Create preconditions - create account, to Transactions table exists
    with ParaBankAPIClient(base_url=base_url, user_data=user_1) as api_client:
        # Get customer ID
        customer_id = api_client.get_customer_id(
            username=user_1["username"], password=user_1["password"]
        )

        # Get existing account Id
        accounts_response = api_client.get_accounts_by_customer_id(customer_id)
        account_id = accounts_response["data"][0]["id"]

        # Create destination account to ensure Transactions table exists
        api_client.create_account(
            customer_id=customer_id,
            from_account_id=account_id,
            account_type=AccountType.CHECKING,
        )

    home_page = HomePage(page, base_url)
    overview_page = OverviewPage(page, base_url)
    activity_page = ActivityPage(page, base_url)

    with allure.step("Login"):
        home_page.login(user_1["username"], user_1["password"])

    with allure.step("Open the first available account from the account list"):
        overview_page.account_links.first.click()

    with allure.step("Validate: Account number"):
        expect(activity_page.account_number_label).to_be_visible()
        expect(activity_page.account_number_value).to_be_visible()

    with allure.step("Validate: Balance"):
        expect(activity_page.balance_label).to_be_visible()
        expect(activity_page.balance_value).to_be_visible()

    with allure.step("Validate: Account type"):
        expect(activity_page.account_type_label).to_be_visible()
        expect(activity_page.account_type_value).to_be_visible()

    with allure.step("Validate: Transactions table is displayed"):
        expect(activity_page.transactions_table).to_be_visible()
