import allure
import pytest

from pages.careers_page import CareersPage


@allure.epic("Claroty Public Website")
@allure.feature("Careers")
@pytest.mark.smoke
@pytest.mark.regression
class TestCareers:
    @allure.title("Careers page displays Join Our Team")
    @allure.story("Careers page")
    @allure.description("Verifies the careers page loads and displays the stable Join Our Team heading.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "careers")
    def test_careers_page_loads_and_displays_join_our_team(self, page, config) -> None:
        careers_page = CareersPage(page, config.base_url)
        careers_page.open()
        careers_page.assert_loaded()

    @allure.title("Current openings link is visible and valid")
    @allure.story("Careers openings")
    @allure.description("Verifies the View Current Openings link is visible and has a valid destination.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "careers", "openings")
    def test_view_current_openings_link_is_visible_and_valid(self, page, config) -> None:
        careers_page = CareersPage(page, config.base_url)
        careers_page.open()
        careers_page.assert_current_openings_link()
