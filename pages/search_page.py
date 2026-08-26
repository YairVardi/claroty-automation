from __future__ import annotations

import re

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage


class SearchPage(BasePage):
    path = "/search"

    @property
    def search_input(self):
        return self.page.get_by_placeholder("Enter search terms")

    @property
    def search_button(self):
        return self.page.get_by_role("button", name="Search")

    def search(self, term: str) -> None:
        with allure.step(f"Search for safe term: {term}"):
            self.search_input.fill(term)
            self.search_button.click()
            expect(self.page).to_have_url(re.compile(rf"/search\?q={re.escape(term)}"))

    def assert_results_for(self, term: str) -> None:
        with allure.step(f"Verify search results are displayed for {term}"):
            expect(self.page.get_by_role("heading", name=re.compile(rf"results for .{re.escape(term)}", re.I))).to_be_visible()
            expect(self.page.get_by_role("link", name=re.compile(re.escape(term), re.I)).first).to_be_visible()
