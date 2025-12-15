import allure
from src.clients.parabank_api_client import ParaBankAPIClient
from src.services.response_validation_service import ResponseValidationService
from src.enums.account_types import AccountType
from src.schemas.parabank_schemas import ParaBankSchemas


def test_get_account_details(base_url, user_1):
    """Test retrieving account details for a specific customer with validation."""

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
        accounts_response = api_client.get_accounts_by_customer_id(customer_id)
        # Use accountId from the previous test
        account_id = accounts_response["data"][0]["id"]

        with allure.step("Call /accounts/{id}"):
            account_details = api_client.get_account_details(account_id)

        with allure.step("Validate: Correct account ID"):
            account_data = account_details["data"]
            assert account_data["id"] == account_id
        # Validate:
        # Correct account ID
        # Balance field
        # Correct data types
        with allure.step("Validate: Balance field"):
            assert "balance" in account_data

        with allure.step("Validate: Correct data types"):
            assert isinstance(account_data["id"], int)
            assert isinstance(account_data["customerId"], int)
            assert isinstance(account_data["type"], str)
            assert isinstance(account_data["balance"], (int, float))
            assert account_data["type"] in [
                account_type.value for account_type in AccountType
            ]

            # Schema validation
            validation_result = validator.validate_response(
                account_data, ParaBankSchemas.get_account_schema()
            )

            assert validation_result[
                "valid"
            ], f"Schema validation failed: {validation_result.get('errors')}"
