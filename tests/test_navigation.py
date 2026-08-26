import allure
import pytest

from pages.home_page import HomePage


@allure.epic("Claroty Public Website")
@allure.feature("Navigation")
@pytest.mark.smoke
@pytest.mark.navigation
@pytest.mark.regression
class TestNavigation:
    @allure.title("Main navigation exposes important internal links")
    @allure.story("Header navigation")
    @allure.description("Verifies stable top navigation links and their internal destinations.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "navigation")
    def test_main_navigation_menus_and_internal_links(self, page, config, test_data) -> None:
        home_page = HomePage(page, config.base_url)
        home_page.open()
        home_page.header.assert_important_links(test_data["important_internal_links"])

    @allure.title("Request a Demo CTA navigates to request-a-demo")
    @allure.story("CTA navigation")
    @allure.description("Verifies the header Request a Demo CTA opens the request demo page.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "cta")
    def test_request_demo_cta_navigates_to_request_demo_page(self, page, config) -> None:
        home_page = HomePage(page, config.base_url)
        home_page.open()
        home_page.header.go_to_request_demo()

    @allure.title("Footer Terms and Privacy links are valid")
    @allure.story("Footer navigation")
    @allure.description("Verifies Terms & Conditions and Privacy Policy footer links.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "footer")
    def test_terms_and_privacy_footer_links(self, page, config, test_data) -> None:
        home_page = HomePage(page, config.base_url)
        home_page.open()
        home_page.footer.assert_policy_links(test_data["footer_links"])
