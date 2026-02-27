import os
import pytest
import requests
import allure
from dotenv import load_dotenv
from playwright.sync_api import Browser
from src.clients.parabank_api_client import ParaBankAPIClient

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    """Returns the base URL for the Parabank application."""
    return os.getenv("BASE_URL", "https://parabank.parasoft.com")


@pytest.fixture(scope="session")
def user_1():
    """Returns user data from environment variables."""
    user_data = {
        "username": os.getenv("USERNAME_1"),
        "password": os.getenv("PASSWORD_1"),
        "full_name": os.getenv("USER_FULLNAME_1"),
    }
    return user_data


@pytest.fixture(scope="function")
def fresh_registered_user(base_url, user_1):
    """Register a fresh user via API client and return complete customer information."""

    # Register the user using the API client
    registration_result = ParaBankAPIClient.register_new_user(base_url, user_1)
    username = registration_result["data"]["username"]
    full_name = registration_result["data"]["full_name"]
    first_name = registration_result["data"]["first_name"]
    last_name = registration_result["data"]["last_name"]
    password = registration_result["data"]["password"]

    if registration_result.get("status_code") != 200:
        raise requests.HTTPError(f"Failed to register user: {registration_result}")

    # Create API client instance for authenticated requests
    with ParaBankAPIClient(base_url=base_url, user_data=user_1) as api_client:
        # Get complete customer information after registration
        customer_id = api_client.get_customer_id(username, user_1["password"])

    return {
        "username": username,
        "full_name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "customer_id": customer_id,
    }


@pytest.fixture(scope="session")
def initialize_db(base_url):
    """Initialize the Parabank Database."""
    yield

    result = ParaBankAPIClient.initialize_database_static(base_url)

    if result.get("status_code") != 204:
        raise requests.HTTPError(f"Failed to initialize database: {result}")


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
