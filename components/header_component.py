from __future__ import annotations

import re

import allure
from playwright.sync_api import Page, expect


class HeaderComponent:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def request_demo_link(self):
        return self.page.get_by_role("link", name="Request a Demo").first

    @property
    def search_link(self):
        return self.page.get_by_role("link", name=re.compile(r"Toggle Search|Search", re.I)).first

    @property
    def menu_button(self):
        return self.page.get_by_role("button", name="Menu").first

    def assert_visible(self) -> None:
        with allure.step("Verify main header is visible"):
            expect(self.request_demo_link).to_be_visible()
            expect(self.search_link).to_be_visible()
            expect(self.page.get_by_role("link", name="Claroty").first).to_be_visible()

    def assert_important_links(self, links: list[dict[str, str]]) -> None:
        with allure.step("Verify important header navigation links"):
            for link in links:
                locator = self.page.get_by_role("link", name=link["name"]).first
                expect(locator).to_be_visible()
                href = locator.get_attribute("href") or ""
                assert link["path"] in href, f"Expected {link['name']} href to include {link['path']}, got {href}"

    def go_to_request_demo(self) -> None:
        with allure.step("Navigate to Request a Demo from header CTA"):
            self.request_demo_link.click()
            expect(self.page).to_have_url(re.compile(r"/request-a-demo/?$"))

    def open_mobile_menu(self) -> None:
        with allure.step("Open mobile navigation menu"):
            self.menu_button.click()
            expect(self.page.get_by_role("button", name="Close Menu")).to_be_visible()
