from src.enums.account_types import AccountType


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
