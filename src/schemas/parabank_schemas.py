from src.enums.account_types import AccountType
from src.enums.transaction_types import TransactionType


class ParaBankSchemas:
    """Collection of JSON schemas for ParaBank API responses."""

    @classmethod
    def get_account_schema(cls):
        """Returns schema for validating a single account."""
        return {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "customerId": {"type": "integer"},
                "type": {
                    "type": "string",
                    "enum": [account_type.value for account_type in AccountType],
                },
                "balance": {"type": "number"},
            },
            "required": ["id", "customerId", "type", "balance"],
        }

    @classmethod
    def get_accounts_list_schema(cls):
        """Returns schema for validating a list of accounts."""
        return {"type": "array", "items": cls.get_account_schema(), "minItems": 1}

    @classmethod
    def get_transaction_schema(cls):
        """Returns schema for validating a single transaction."""
        return {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "accountId": {"type": "integer"},
                "type": {
                    "type": "string",
                    "enum": [t_type.value for t_type in TransactionType],
                },
                "amount": {"type": "number"},
                "date": {"type": "number"},
                "description": {"type": "string"},
            },
            "required": ["id", "accountId", "type", "amount", "date", "description"],
        }

    @classmethod
    def get_transactions_list_schema(cls):
        """Returns schema for validating a list of transactions."""
        return {"type": "array", "items": cls.get_transaction_schema()}
