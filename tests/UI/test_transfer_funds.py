import allure
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.activity_page import ActivityPage
from pages.transfer_page import TransferPage
from src.clients.parabank_api_client import ParaBankAPIClient
from src.enums.account_types import AccountType
from src.utils.currency_utils import format_currency


def test_transfer_funds(page, base_url, fresh_registered_user):
    """Test transferring funds between accounts."""

    # API Setup: Create preconditions - create account, get accounts IDs and balances
    with ParaBankAPIClient(
        base_url=base_url, user_data=fresh_registered_user
    ) as api_client:
        # Get customer ID
        customer_id = fresh_registered_user["customer_id"]

        # Get existing account Id
        accounts_response = api_client.get_accounts_by_customer_id(customer_id)
        source_account_id = accounts_response["data"][0]["id"]

        # Create destination account
        new_account_response = api_client.create_account(
            customer_id=customer_id,
            from_account_id=source_account_id,
            account_type=AccountType.CHECKING,
        )

        # Get balance of source account before transfer
        source_account_details = api_client.get_account_details(source_account_id)
        initial_source_balance = source_account_details["data"]["balance"]

        # Get balance of destination account before transfer
        destination_account_id = new_account_response["data"]["id"]
        destination_account_details = api_client.get_account_details(
            destination_account_id
        )
        destination_account_balance = destination_account_details["data"]["balance"]

    home_page = HomePage(page, base_url)
    activity_page = ActivityPage(page, base_url)
    transfer_page = TransferPage(page, base_url)

    transfer_amount = 3.00

    with allure.step("Login"):
        home_page.login(
            fresh_registered_user["username"], fresh_registered_user["password"]
        )

    with allure.step("Navigate to “Transfer Funds”"):
        transfer_page.goto()

    with allure.step("Transfer an amount (e.g., 10 USD) from one account to another"):
        transfer_page.transfer_funds(
            amount=transfer_amount,
            from_account_id=source_account_id,
            to_account_id=destination_account_id,
        )

    with allure.step("Validate: Success message"):
        expect(transfer_page.result_message).to_contain_text("Transfer Complete!")
        expect(transfer_page.result_message).to_contain_text(
            f"{format_currency(transfer_amount)} has been transferred from account #{source_account_id} to account #{destination_account_id}."
        )

    with allure.step("Validate: Balances changed correctly (before → after)"):
        activity_page.goto(source_account_id)

        # Calculate expected balance and format it correctly
        source_account_expected_balance = initial_source_balance - transfer_amount

        # Check balance changed correctly for source account
        expect(activity_page.balance_value).to_have_text(
            format_currency(source_account_expected_balance)
        )

        # Check balance changed correctly for destination account
        activity_page.goto(destination_account_id)
        expected_destination_balance = destination_account_balance + transfer_amount
        expect(activity_page.balance_value).to_have_text(
            format_currency(expected_destination_balance)
        )
