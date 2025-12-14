from enum import Enum


class AccountType(Enum):
    """Account types supported by ParaBank."""

    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
