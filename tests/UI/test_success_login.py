import allure
from playwright.sync_api import expect
from pages import HomePage, OverviewPage


def test_success_login(page, base_url, fresh_registered_user):
    """Test successful login to the Parabank application."""
    home_page = HomePage(page, base_url)
    overview_page = OverviewPage(page, base_url)

    with allure.step("Open the ParaBank homepage"):
        home_page.goto()

    with allure.step("Login using valid credentials"):
        home_page.customer_login.login(
            fresh_registered_user["username"], fresh_registered_user["password"]
        )

    with allure.step("Validate: The welcome message with customer name"):
        expect(home_page.welcome_message).to_be_visible()
        expect(home_page.welcome_message).to_have_text(
            f"Welcome {fresh_registered_user['full_name']}"
        )

    with allure.step("Validate: Account list is displayed"):
        expect(overview_page.account_list).to_be_visible()
