from __future__ import annotations

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage


class CareersPage(BasePage):
    path = "/careers"
    heading = "Join Our Team"

    @property
    def current_openings_link(self):
        return self.page.get_by_role("link", name="View Current Openings").first

    def assert_loaded(self) -> None:
        self.assert_heading_visible(self.heading)

    def assert_current_openings_link(self) -> None:
        with allure.step("Verify current openings link is visible and has a valid destination"):
            expect(self.current_openings_link).to_be_visible()
            href = self.current_openings_link.get_attribute("href") or ""
            assert href.startswith("http") or href.startswith("/") or href.startswith("#"), f"Unexpected href: {href}"
