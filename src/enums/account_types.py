from enum import Enum


class AccountType(Enum):
    """Account types supported by ParaBank."""

    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
    LOAN = "LOAN"

    @property
    def id(self):
        """Get account type id."""
        mapping = {"CHECKING": 0, "SAVINGS": 1, "LOAN": 2}
        return mapping[self.value]
