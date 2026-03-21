import allure
from playwright.sync_api import expect
from pages import HomePage, OverviewPage


def test_failed_login(page, base_url):
    """Test that login fails with invalid credentials and displays appropriate error messages."""
    with allure.step("Initialize page objects"):
        home_page = HomePage(page, base_url)
        overview_page = OverviewPage(page, base_url)

    with allure.step("Open the ParaBank homepage"):
        home_page.goto()

    with allure.step("Login using invalid credentials"):
        home_page.customer_login.login("invalid_user", "wrong_password")

    with allure.step("Validate: An error message is displayed"):
        expect(home_page.error_message).to_be_visible()
        expect(home_page.error_message).to_have_text(
            "The username and password could not be verified."
        )

    with allure.step("Validate: Accounts page is not accessible"):
        expect(overview_page.account_list).to_have_count(0)
        overview_page.goto()
        expect(overview_page.account_list).to_have_count(0)
        expect(home_page.error_message).to_have_text(
            "An internal error has occurred and has been logged."
        )
