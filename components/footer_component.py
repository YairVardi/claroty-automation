from __future__ import annotations

import allure
from playwright.sync_api import Page, expect


class FooterComponent:
    def __init__(self, page: Page) -> None:
        self.page = page

    def assert_visible(self) -> None:
        with allure.step("Verify footer is visible"):
            footer = self.page.get_by_role("contentinfo")
            expect(footer).to_be_visible()
            expect(footer.get_by_text("Claroty. All rights reserved.")).to_be_visible()
            expect(footer.get_by_role("link", name="Claroty xDome Platform")).to_be_visible()
            expect(footer.get_by_role("link", name="About Us")).to_be_visible()

    def assert_policy_links(self, links: list[dict[str, str]]) -> None:
        with allure.step("Verify footer policy links"):
            footer = self.page.get_by_role("contentinfo")
            for link in links:
                locator = footer.get_by_role("link", name=link["name"])
                expect(locator).to_be_visible()
                href = locator.get_attribute("href") or ""
                assert link["path"] in href, f"Expected {link['name']} href to include {link['path']}, got {href}"
