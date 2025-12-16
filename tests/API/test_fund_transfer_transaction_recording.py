import allure
from src.clients.parabank_api_client import ParaBankAPIClient
from src.enums.account_types import AccountType
from src.services.response_validation_service import ResponseValidationService
from src.schemas.parabank_schemas import ParaBankSchemas


def test_get_transactions(base_url, fresh_registered_user):
    """Test fund transfer creates correct debit/credit transactions in both accounts with schema validation."""
    # Initialize API client and validator

    validator = ResponseValidationService()
    transfer_amount = 51.10

    with ParaBankAPIClient(
        base_url=base_url,
        user_data=fresh_registered_user,
    ) as api_client:

        # Get customer ID
        customer_id = fresh_registered_user["customer_id"]

        accounts_response = api_client.get_accounts_by_customer_id(customer_id)
        source_account_id = accounts_response["data"][0]["id"]

        new_account_response = api_client.create_account(
            customer_id=customer_id,
            from_account_id=source_account_id,
            account_type=AccountType.SAVINGS,
        )
        destination_account_id = new_account_response["data"]["id"]

        with allure.step("Send POST to transfer funds between accounts"):
            api_client.transfer_funds(
                from_account_id=source_account_id,
                to_account_id=destination_account_id,
                amount=transfer_amount,
            )

        with allure.step("Call /accounts/{account_id}/transactions for source account"):
            source_transactions_response = api_client.get_transactions_by_account_id(
                source_account_id
            )

        with allure.step("Validate: Status code 200 "):
            assert source_transactions_response["status_code"] == 200

        with allure.step("Validate: Transactions schema"):
            source_transactions = source_transactions_response["data"]
            validation_result = validator.validate_response(
                source_transactions,
                ParaBankSchemas.get_transactions_list_schema(),
            )

            assert validation_result[
                "valid"
            ], f"Schema validation failed: {validation_result.get('errors')}"

        with allure.step("Validate: Recent transfer in source account"):
            recent_source_transaction = source_transactions[-1]
            assert recent_source_transaction["type"] == "Debit"
            assert recent_source_transaction["amount"] == transfer_amount
            assert recent_source_transaction["description"] == "Funds Transfer Sent"

        with allure.step(
            "Call /accounts/{account_id}/transactions for destination account"
        ):
            destination_transactions_response = (
                api_client.get_transactions_by_account_id(destination_account_id)
            )

        with allure.step("Validate: Status code 200"):
            assert destination_transactions_response["status_code"] == 200

        with allure.step("Validate: Transactions schema"):
            destination_transactions = destination_transactions_response["data"]
            validation_result = validator.validate_response(
                destination_transactions,
                ParaBankSchemas.get_transactions_list_schema(),
            )

            assert validation_result[
                "valid"
            ], f"Schema validation failed: {validation_result.get('errors')}"

        with allure.step("Validate: Recent transfer in destination account"):
            recent_destination_transaction = destination_transactions[-1]
            assert recent_destination_transaction["type"] == "Credit"
            assert recent_destination_transaction["amount"] == transfer_amount
            assert (
                recent_destination_transaction["description"]
                == "Funds Transfer Received"
            )
