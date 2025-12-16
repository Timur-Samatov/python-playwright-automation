import requests
from os import urandom
from src.utils.encoding_utils import encode_credentials
from src.enums.account_types import AccountType


class ParaBankAPIClient:
    """API client wrapper for ParaBank banking operations."""

    def __init__(self, base_url, user_data):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Authorization": f"Basic {encode_credentials(user_data['username'], user_data['password'])}",
            }
        )

    @staticmethod
    def initialize_database_static(base_url):
        """
        Initialize the ParaBank database without authentication.
        Static method for utility/cleanup operations.
        """
        url = f"{base_url}/parabank/services/bank/initializeDB"
        response = requests.post(url)

        try:
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "data": response.text,
            }
        except requests.RequestException as e:
            return {
                "status_code": getattr(response, "status_code", None),
                "error": str(e),
                "data": getattr(response, "text", None),
            }

    @staticmethod
    def register_new_user(base_url, user_data, unique_suffix=True):
        """
        Register a new user via HTTP form submission.
        Static method for user registration without authentication.

        Args:
            base_url (str): ParaBank base URL
            user_data (dict): User information containing username, password, full_name

        Returns:
            dict: Registration result with user info
        """
        session = requests.Session()

        try:
            # Hit register page to obtain cookies (JSESSIONID)
            landing = session.get(
                f"{base_url}/parabank/register.htm", allow_redirects=True
            )
            landing.raise_for_status()

            # Parse full name into first and last name
            full_name = user_data["full_name"]
            name_parts = full_name.split(" ")
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            # Generate unique username and first name if required
            if unique_suffix:
                username = user_data["username"] + str(urandom(4).hex())
                first_name = first_name + str(urandom(2).hex())
                last_name = last_name + str(urandom(2).hex())
                full_name = first_name + " " + last_name

            # Prepare registration payload
            payload = {
                "customer.firstName": first_name,
                "customer.lastName": last_name,
                "customer.address.street": "123 Test Street",
                "customer.address.city": "Test City",
                "customer.address.state": "TS",
                "customer.address.zipCode": "12345",
                "customer.phoneNumber": "5551234567",
                "customer.ssn": "11111111",
                "customer.username": username,
                "customer.password": user_data["password"],
                "repeatedPassword": user_data["password"],
            }

            # Submit registration form
            register_resp = session.post(
                f"{base_url}/parabank/register.htm",
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                allow_redirects=True,
            )
            register_resp.raise_for_status()

            return {
                "status_code": register_resp.status_code,
                "data": {
                    "username": username,
                    "password": user_data["password"],
                    "full_name": full_name,
                    "first_name": first_name,
                    "last_name": last_name,
                },
            }

        except requests.RequestException as e:
            return {
                "status_code": (
                    getattr(register_resp, "status_code", None)
                    if "register_resp" in locals()
                    else None
                ),
                "error": str(e),
                "data": None,
            }
        finally:
            session.close()

    def _handle_response(self, response):
        """Handle API response and extract relevant data."""
        try:
            response.raise_for_status()

            # Try to parse JSON if content type indicates JSON
            data = response.text
            if response.headers.get("content-type", "").startswith("application/json"):
                try:
                    data = response.json()
                except ValueError:
                    pass

            return {"status_code": response.status_code, "data": data}

        except requests.RequestException as e:
            return {
                "status_code": getattr(response, "status_code", None),
                "error": str(e),
                "data": getattr(response, "text", None),
            }

    def get_customer_info(self, username, password):
        """Retrieve customer information by username/password."""
        url = f"{self.base_url}/parabank/services/bank/login/{username}/{password}"
        response = self.session.get(url)
        return self._handle_response(response)

    def get_customer_id(self, username, password):
        """Retrieve customer ID by username and password."""
        response = self.get_customer_info(username, password)
        return response["data"]["id"]

    def get_accounts_by_customer_id(self, customer_id):
        """Retrieve all accounts for a customer."""
        url = f"{self.base_url}/parabank/services/bank/customers/{customer_id}/accounts"
        response = self.session.get(url)
        return self._handle_response(response)

    def get_account_details(self, account_id):
        """Get detailed information for a specific account."""
        url = f"{self.base_url}/parabank/services/bank/accounts/{account_id}"
        response = self.session.get(url)
        return self._handle_response(response)

    def transfer_funds(self, from_account_id, to_account_id, amount):
        """
        Transfer funds between accounts.

        Args:
            from_account_id (int): Source account ID
            to_account_id (int): Destination account ID
            amount (int, float): Amount to transfer

        Returns:
            message: Successfully transferred ${amount} from account #{from_account_id} to account #{to_account_id}
        """
        url = f"{self.base_url}/parabank/services/bank/transfer"
        params = {
            "fromAccountId": from_account_id,
            "toAccountId": to_account_id,
            "amount": str(amount),
        }

        response = self.session.post(url, params=params)
        return self._handle_response(response)

    def create_account(
        self, customer_id, from_account_id, account_type=AccountType.CHECKING
    ):
        """
        Create a new account for a customer.

        Args:
            customer_id (int): Customer identifier
            from_account_id (int): Source account for initial deposit
            account_type (AccountType): Type of account to create
            from_account_id (int): Source account for initial deposit

        Returns:
            dict: New account information
        """
        url = f"{self.base_url}/parabank/services/bank/createAccount"

        # Convert the string AccountType (e.g., 'CHECKING') into its required integer API representation.
        if isinstance(account_type, AccountType):
            account_type_id = account_type.id
        else:
            raise ValueError(f"Expected AccountType, got: {type(account_type)}")

        params = {
            "customerId": customer_id,
            "newAccountType": account_type_id,
            "fromAccountId": from_account_id,
        }

        response = self.session.post(url, params=params)
        return self._handle_response(response)

    def get_transactions_by_account_id(self, account_id):
        """Retrieve transactions for a specific account."""
        url = (
            f"{self.base_url}/parabank/services/bank/accounts/{account_id}/transactions"
        )
        response = self.session.get(url)
        return self._handle_response(response)

    def close(self):
        """Close the HTTP session and cleanup resources."""
        if self.session:
            self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with automatic cleanup."""
        self.close()
