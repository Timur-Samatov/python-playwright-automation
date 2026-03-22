import allure
from playwright.sync_api import sync_playwright
from axe_core_python.sync_playwright import Axe
from pages import HomePage


def test_page_accessibility(page, base_url):
    home_page = HomePage(page, base_url)

    with allure.step("Open home page"):
        home_page.goto()

    with allure.step("Run axe-core accessibility scan"):
        axe = Axe()
        results = axe.run(page)

    violations = results["violations"]
    if violations:
        allure.attach(str(violations), name="axe_violations", attachment_type=allure.attachment_type.JSON)

    with allure.step("Assert no accessibility violations"):
        assert len(violations) == 0, f"Accessibility violations found: {violations}"
