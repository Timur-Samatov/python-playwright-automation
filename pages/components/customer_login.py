class CustomerLogin:
    """Page Object Model for the customer login form component."""

    def __init__(self, page):
        self.page = page
        # Locators
        self.username_input = self.page.locator("[name='username']")
        self.password_input = self.page.locator("[name='password']")
        self.login_button = self.page.locator("input[value='Log In']")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
