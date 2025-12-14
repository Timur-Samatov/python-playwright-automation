import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.overview_page import OverviewPage


def test_success_login(page, base_url, user_1):
    home_page = HomePage(page, base_url)
    overview_page = OverviewPage(page, base_url)

    # Open the ParaBank homepage
    home_page.goto()

    # Login using valid credentials
    home_page.customer_login.login(user_1["username"], user_1["password"])

    # Validate:
    # The welcome message with customer name
    expect(home_page.welcome_message).to_be_visible()
    expect(home_page.welcome_message).to_have_text(f"Welcome {user_1['full_name']}")

    # Account list is displayed
    expect(overview_page.account_table).to_be_visible()


def test_invalid_login(page, base_url):
    home_page = HomePage(page, base_url)

    # Open the ParaBank homepage
    home_page.goto()

    # Login using invalid credentials
    home_page.customer_login.login("invalid_user", "wrong_password")

    # Validate:
    # An error message is displayed
    expect(home_page.error_message).to_be_visible()
    expect(home_page.error_message).to_have_text(
        "The username and password could not be verified."
    )
