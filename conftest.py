import os
import pytest
import requests
import allure
from dotenv import load_dotenv
from playwright.sync_api import Browser

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    """Returns the base URL for the Parabank application."""
    return "https://parabank.parasoft.com"


@pytest.fixture(scope="session")
def user_1():
    """Returns user data from environment variables."""
    user_data = {
        "username": os.getenv("USERNAME_1"),
        "password": os.getenv("PASSWORD_1"),
        "full_name": os.getenv("USER_FULLNAME_1"),
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


@pytest.fixture(scope="function")
def page(browser: Browser, request):
    """Create a new browser context and page for each test, with tracing enabled."""

    # Create a new browser context
    context = browser.new_context()

    # Enable tracing for the context
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    yield page

    # Capture trace after test
    # Save trace to a file
    test_name = request.node.name
    context.tracing.stop(path=f"test-results/traces/{test_name}_trace.zip")

    # Close context
    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Enhanced test failure reporting with screenshots."""
    outcome = yield
    report = outcome.get_result()

    # Handle test failures during the call phase
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page:
            # Save screenshot
            screenshot_path = (
                f"test-results/screenshots/{item.nodeid.replace('::', '_')}.png"
            )
            page.screenshot(path=screenshot_path)

            # Attach screenshot to Allure report
            allure.attach.file(
                screenshot_path,
                name="Screenshot on failure",
                attachment_type=allure.attachment_type.PNG,
            )
