import requests
from tests.utils.encoding_utils import encode_credentials
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

            return {
                "status_code": response.status_code,
                "data": data,
                "cookies": self.session.cookies.get_dict(),
                "session_id": self.session.cookies.get("JSESSIONID"),
            }

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
        """
        Get detailed information for a specific account.

        Args:
            account_id (str): Account identifier

        Returns:
            dict: Account details including balance and type
        """
        url = f"{self.base_url}/parabank/services/bank/accounts/{account_id}"
        response = self.session.get(url)
        return self._handle_response(response)

    def get_transaction_history(self, account_id):
        """
        Get transaction history for an account.

        Args:
            account_id (str): Account identifier

        Returns:
            dict: List of transactions
        """
        url = (
            f"{self.base_url}/parabank/services/bank/accounts/{account_id}/transactions"
        )
        response = self.session.get(url)
        return self._handle_response(response)

    def get_transaction_details(self, transaction_id):
        """
        Get detailed information for a specific transaction.

        Args:
            transaction_id (str): Transaction identifier

        Returns:
            dict: Transaction details
        """
        url = f"{self.base_url}/parabank/services/bank/transactions/{transaction_id}"
        response = self.session.get(url)
        return self._handle_response(response)

    def transfer_funds(self, from_account_id, to_account_id, amount):
        """
        Transfer funds between accounts.

        Args:
            from_account_id (str): Source account ID
            to_account_id (str): Destination account ID
            amount (float): Amount to transfer

        Returns:
            dict: Transfer result
        """
        url = f"{self.base_url}/parabank/services/bank/transfer"
        params = {
            "fromAccountId": from_account_id,
            "toAccountId": to_account_id,
            "amount": str(amount),
        }

        response = self.session.post(url, params=params)
        return self._handle_response(response)

    def withdraw_funds(self, account_id, amount):
        """
        Withdraw funds from an account.

        Args:
            account_id (str): Account identifier
            amount (float): Amount to withdraw

        Returns:
            dict: Withdrawal result
        """
        url = f"{self.base_url}/parabank/services/bank/withdraw"
        params = {"accountId": account_id, "amount": str(amount)}

        response = self.session.post(url, params=params)
        return self._handle_response(response)

    def deposit_funds(self, account_id, amount):
        """
        Deposit funds to an account.

        Args:
            account_id (str): Account identifier
            amount (float): Amount to deposit

        Returns:
            dict: Deposit result
        """
        url = f"{self.base_url}/parabank/services/bank/deposit"
        params = {"accountId": account_id, "amount": str(amount)}

        response = self.session.post(url, params=params)
        return self._handle_response(response)

    def create_account(
        self, customer_id, account_type=AccountType.CHECKING, from_account_id=None
    ):
        """
        Create a new account for a customer.

        Args:
            customer_id (str): Customer identifier
            account_type (AccountType): Type of account to create
            from_account_id (str, optional): Source account for initial deposit

        Returns:
            dict: New account information
        """
        url = f"{self.base_url}/parabank/services/bank/createAccount"
        params = {
            "customerId": customer_id,
            "newAccountType": (
                account_type.value
                if isinstance(account_type, AccountType)
                else account_type
            ),
        }

        if from_account_id:
            params["fromAccountId"] = from_account_id

        response = self.session.post(url, params=params)
        return self._handle_response(response)

    def request_loan(self, customer_id, amount, down_payment, from_account_id):
        """
        Request a loan for a customer.

        Args:
            customer_id (str): Customer identifier
            amount (float): Loan amount requested
            down_payment (float): Down payment amount
            from_account_id (str): Account for down payment

        Returns:
            dict: Loan application result
        """
        url = f"{self.base_url}/parabank/services/bank/requestLoan"
        params = {
            "customerId": customer_id,
            "amount": str(amount),
            "downPayment": str(down_payment),
            "fromAccountId": from_account_id,
        }

        response = self.session.post(url, params=params)
        return self._handle_response(response)

    def pay_bill(
        self,
        account_id,
        amount,
        payee_name,
        payee_address,
        payee_city,
        payee_state,
        payee_zip,
        payee_phone,
        payee_account,
    ):
        """
        Pay a bill from an account.

        Args:
            account_id (str): Account to pay from
            amount (float): Payment amount
            payee_name (str): Payee name
            payee_address (str): Payee street address
            payee_city (str): Payee city
            payee_state (str): Payee state
            payee_zip (str): Payee ZIP code
            payee_phone (str): Payee phone number
            payee_account (str): Payee account number

        Returns:
            dict: Bill payment result
        """
        url = f"{self.base_url}/parabank/services/bank/billpay"
        params = {
            "accountId": account_id,
            "amount": str(amount),
            "payee.name": payee_name,
            "payee.address.street": payee_address,
            "payee.address.city": payee_city,
            "payee.address.state": payee_state,
            "payee.address.zipCode": payee_zip,
            "payee.phoneNumber": payee_phone,
            "payee.accountNumber": payee_account,
        }

        response = self.session.post(url, params=params)
        return self._handle_response(response)

    def find_transactions(
        self, account_id, transaction_type=None, amount=None, date_range=None
    ):
        """
        Find transactions by criteria.

        Args:
            account_id (str): Account identifier
            transaction_type (str, optional): Type of transaction to find
            amount (float, optional): Specific amount to search for
            date_range (dict, optional): Date range with 'from' and 'to' keys

        Returns:
            dict: Matching transactions
        """
        base_url = (
            f"{self.base_url}/parabank/services/bank/accounts/{account_id}/transactions"
        )

        if transaction_type:
            url = (
                f"{base_url}/onDate/{date_range['date']}"
                if date_range and "date" in date_range
                else f"{base_url}/month/{transaction_type}"
            )
        elif amount:
            url = f"{base_url}/amount/{amount}"
        elif date_range:
            url = f"{base_url}/fromDate/{date_range['from']}/toDate/{date_range['to']}"
        else:
            url = base_url

        response = self.session.get(url)
        return self._handle_response(response)

    # def reset_database(self):
    #     """
    #     Reset the ParaBank database (useful for testing).

    #     Returns:
    #         dict: Reset operation result
    #     """
    #     url = f"{self.base_url}/parabank/services/bank/initializeDB"
    #     response = self.session.post(url)
    #     return self._handle_response(response)

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
