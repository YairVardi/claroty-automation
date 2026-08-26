import allure
import pytest

from pages.home_page import HomePage


@allure.epic("Claroty Public Website")
@allure.feature("Home Page")
@pytest.mark.smoke
@pytest.mark.regression
class TestHomePage:
    @allure.title("Claroty homepage loads successfully")
    @allure.story("Homepage availability")
    @allure.description("Verifies the Claroty homepage loads and displays the stable main heading.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "home")
    def test_homepage_loads_successfully(self, page, config) -> None:
        home_page = HomePage(page, config.base_url)
        home_page.open()
        home_page.assert_loaded()

    @allure.title("Homepage title contains Claroty")
    @allure.story("Page metadata")
    @allure.description("Verifies the browser title contains Claroty.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "title")
    def test_homepage_title_contains_claroty(self, page, config, test_data) -> None:
        home_page = HomePage(page, config.base_url)
        home_page.open()
        home_page.assert_title_contains(test_data["expected"]["home_title_keyword"])

    @allure.title("Homepage main heading is visible")
    @allure.story("Hero content")
    @allure.description("Verifies the stable homepage H1 is visible.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "heading")
    def test_main_homepage_heading_is_visible(self, page, config, test_data) -> None:
        home_page = HomePage(page, config.base_url)
        home_page.open()
        home_page.assert_heading_visible(test_data["expected"]["home_heading"])

    @allure.title("Homepage header and footer are visible")
    @allure.story("Shared layout")
    @allure.description("Verifies stable header controls and footer sections.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "layout")
    def test_main_header_and_footer_are_visible(self, page, config) -> None:
        home_page = HomePage(page, config.base_url)
        home_page.open()
        home_page.header.assert_visible()
        home_page.footer.assert_visible()
