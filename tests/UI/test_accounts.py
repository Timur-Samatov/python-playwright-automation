import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.overview_page import OverviewPage
from pages.activity_page import ActivityPage


def test_view_account_details(page, base_url, user_1):
    home_page = HomePage(page, base_url)
    overview_page = OverviewPage(page, base_url)
    activity_page = ActivityPage(page, base_url)
    # Login
    home_page.login(user_1["username"], user_1["password"])
    # Open the first available account from the account list
    overview_page.account_links.first.click()
    # Validate:
    # Account number
    expect(activity_page.account_number_label).to_be_visible()
    expect(activity_page.account_number_value).to_be_visible()
    # Balance
    expect(activity_page.balance_label).to_be_visible()
    expect(activity_page.balance_value).to_be_visible()
    # Account type
    expect(activity_page.account_type_label).to_be_visible()
    expect(activity_page.account_type_value).to_be_visible()
    # Transactions table is displayed
    pass
