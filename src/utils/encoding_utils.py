import base64


def encode_to_base64(data):
    """
    Encode string or bytes to base64.

    Args:
        data (str or bytes): Data to encode

    Returns:
        str: Base64 encoded string
    """
    if isinstance(data, str):
        data = data.encode("utf-8")

    return base64.b64encode(data).decode("utf-8")


def encode_credentials(username, password):
    """
    Encode username:password for Basic Auth.

    Args:
        username (str): Username
        password (str): Password

    Returns:
        str: Base64 encoded credentials
    """
    credentials = f"{username}:{password}"
    return encode_to_base64(credentials)
