import allure
from src.clients.parabank_api_client import ParaBankAPIClient
from src.services.response_validation_service import ResponseValidationService
from src.enums.account_types import AccountType
from src.schemas.parabank_schemas import ParaBankSchemas


def test_create_new_account(base_url, user_1):
    """Test creating a new account for a customer with response validation."""

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

        with allure.step("Send POST to create a new account"):
            new_account_response = api_client.create_account(
                customer_id=customer_id,
                from_account_id=account_id,
                account_type=AccountType.SAVINGS,
            )

        with allure.step("Validate: 200/201 status"):
            assert new_account_response["status_code"] in [200, 201]

        with allure.step("Validate: Correct fields in response"):
            new_account_data = new_account_response["data"]
            assert new_account_data["customerId"] == customer_id

            # Schema validation
            validation_result = validator.validate_response(
                new_account_data, ParaBankSchemas.get_account_schema()
            )

            assert validation_result[
                "valid"
            ], f"Schema validation failed: {validation_result.get('errors')}"
