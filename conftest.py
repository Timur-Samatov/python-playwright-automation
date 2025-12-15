import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    """Returns the base URL for the Parabank application."""
    return "https://parabank.parasoft.com"


@pytest.fixture(scope="session")
def user_1():
    """Returns user data from environment variables."""
    user_data = {
        "username": os.getenv("PLAYWRIGHT_USERNAME_1"),
        "password": os.getenv("PLAYWRIGHT_PASSWORD_1"),
        "full_name": os.getenv("PLAYWRIGHT_USER_FULLNAME_1"),
    }
    return user_data


@pytest.fixture(scope="session", autouse=True)
def registered_user(base_url, user_1):
    """Register a fresh user via HTTP and return credentials + session cookie."""

    session = requests.Session()

    # Hit register page to obtain cookies (JSESSIONID)
    landing = session.get(f"{base_url}/parabank/register.htm", allow_redirects=True)
    landing.raise_for_status()

    first_name = user_1["full_name"].split(" ")[0]
    last_name = user_1["full_name"].split(" ")[1]

    payload = {
        "customer.firstName": first_name,
        "customer.lastName": last_name,
        "customer.address.street": "Some address",
        "customer.address.city": "Some City",
        "customer.address.state": "TS",
        "customer.address.zipCode": "12345",
        "customer.phoneNumber": "5551234567",
        "customer.ssn": "11111111",
        "customer.username": user_1["username"],
        "customer.password": user_1["password"],
        "repeatedPassword": user_1["password"],
    }

    register_resp = session.post(
        f"{base_url}/parabank/register.htm",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        allow_redirects=True,
    )
    register_resp.raise_for_status()

    return {
        "username": user_1["username"],
        "password": user_1["password"],
        "full_name": user_1["full_name"],
        "session_id": session.cookies.get("JSESSIONID"),
        "cookies": session.cookies.get_dict(),
    }


@pytest.fixture(scope="session", autouse=True)
def initialize_db(base_url):
    """Reset Parabank DB after the test session finishes."""
    yield
    response = requests.post(f"{base_url}/parabank/services/bank/initializeDB")
    response.raise_for_status()


# Fixtures run in definition order; registered_user happens first, initialize_db cleanup happens last
