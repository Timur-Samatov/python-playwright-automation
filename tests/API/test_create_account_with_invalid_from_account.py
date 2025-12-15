import allure
from src.clients.parabank_api_client import ParaBankAPIClient
from src.services.response_validation_service import ResponseValidationService
from src.enums.account_types import AccountType


def test_create_account_with_invalid_from_account_id(base_url, user_1):
    """Test that creating a new account fails when using a non-existent from_account_id"""

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
        # Use a non-existent account ID to trigger validation error
        non_existent_account_id = 9999999

        with allure.step(
            "Attempt to create a new account with invalid from_account_id"
        ):  #
            new_account_response = api_client.create_account(
                customer_id=customer_id,
                from_account_id=non_existent_account_id,
                account_type=AccountType.SAVINGS,
            )

        with allure.step("Validate: Correct 4xx error"):
            assert new_account_response["status_code"] == 400

        with allure.step("Validate: Error message in response"):
            error_data = new_account_response["data"]
            expected_error = (
                f"Could not create new account for customer {customer_id} "
                f"from account {non_existent_account_id}"
            )

            assert error_data == expected_error
