def format_currency(amount):
    """
    Formats a currency amount as a string, handling ParaBank's negative format.

    Args:
        amount (float): The monetary amount to format

    Returns:
        str: Formatted currency string (e.g., "$123.45" or "-$123.45")

    Examples:
        >>> format_currency(123.45)
        '$123.45'
        >>> format_currency(-123.45)
        '-$123.45'
        >>> format_currency(0)
        '$0.00'
    """
    if amount < 0:
        return f"-${abs(amount):.2f}"
    else:
        return f"${amount:.2f}"
