from enum import Enum


class TransactionType(Enum):
    """Transaction types supported by ParaBank."""

    DEBIT = "Debit"
    CREDIT = "Credit"
