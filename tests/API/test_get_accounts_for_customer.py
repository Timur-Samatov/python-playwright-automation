import allure
from src.clients.parabank_api_client import ParaBankAPIClient
from src.services.response_validation_service import ResponseValidationService
from src.enums.account_types import AccountType
from src.schemas.parabank_schemas import ParaBankSchemas


def test_get_accounts_for_customer(base_url, user_1):
    """Test retrieving accounts list for a customer with validation."""

    # Initialize API client and validator
    validator = ResponseValidationService()

    with ParaBankAPIClient(
        base_url=base_url,
        user_data=user_1,
    ) as api_client:

        # Get customer ID
        customer_id = api_client.get_customer_id(
            username=user_1["username"], password=user_1["password"]
        )

        with allure.step("Call /accounts?customerId={id} or similar endpoint"):
            accounts_response = api_client.get_accounts_by_customer_id(customer_id)

        with allure.step("Validate: Status code 200"):
            assert accounts_response["status_code"] == 200

        with allure.step("Validate: Non-empty list of accounts"):
            accounts_data = accounts_response["data"]
            assert isinstance(accounts_data, list), "Expected list of accounts"
            assert len(accounts_data) > 0, "Customer should have at least one account"

        with allure.step("Validate: Each account has required fields"):
            for account in accounts_data:
                assert "id" in account
                assert "type" in account
                assert "balance" in account
                assert account["type"] in [
                    account_type.value for account_type in AccountType
                ]

            # Schema validation
            validation_result = validator.validate_response(
                accounts_data, ParaBankSchemas.get_accounts_list_schema()
            )

            assert validation_result[
                "valid"
            ], f"Schema validation failed: {validation_result.get('errors')}"
