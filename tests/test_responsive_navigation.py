import allure
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@allure.epic("Claroty Public Website")
@allure.feature("Responsive Navigation")
@pytest.mark.smoke
@pytest.mark.responsive
@pytest.mark.navigation
@pytest.mark.regression
def test_mobile_navigation_menu(page, config) -> None:
    allure.dynamic.title("Mobile navigation menu opens and shows key links")
    allure.dynamic.story("Mobile menu")
    allure.dynamic.description("Uses a mobile viewport and verifies the menu opens with stable navigation links.")
    allure.dynamic.severity(allure.severity_level.NORMAL)
    allure.dynamic.tag("smoke", "responsive", "mobile-navigation")

    page.set_viewport_size({"width": 390, "height": 844})
    home_page = HomePage(page, config.base_url)
    home_page.open()
    home_page.header.open_mobile_menu()
    expect(page.get_by_role("link", name="Careers").last).to_be_visible()
    expect(page.get_by_role("link", name="Search").last).to_be_visible()
