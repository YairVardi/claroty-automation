import allure
import pytest

from pages.search_page import SearchPage


@allure.epic("Claroty Public Website")
@allure.feature("Search")
@pytest.mark.smoke
@pytest.mark.regression
class TestSearch:
    @allure.title("Search works for safe xDome term")
    @allure.story("Site search")
    @allure.description("Verifies the site search returns stable results for the safe term xDome.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "search")
    def test_search_functionality_with_safe_term(self, page, config, test_data) -> None:
        search_page = SearchPage(page, config.base_url)
        search_page.open()
        term = test_data["safe_search_term"]
        search_page.search(term)
        search_page.assert_results_for(term)
