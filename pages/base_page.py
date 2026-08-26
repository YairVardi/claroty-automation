from __future__ import annotations

import re

import allure
from playwright.sync_api import Page, expect

from components.cookie_banner_component import CookieBannerComponent
from components.footer_component import FooterComponent
from components.header_component import HeaderComponent


class BasePage:
    path = "/"

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.header = HeaderComponent(page)
        self.footer = FooterComponent(page)
        self.cookie_banner = CookieBannerComponent(page)

    @property
    def url(self) -> str:
        return f"{self.base_url}{self.path}"

    def open(self) -> None:
        with allure.step(f"Open {self.url}"):
            self.page.goto(self.url, wait_until="load")
            self.cookie_banner.handle_if_visible()

    def assert_title_contains(self, text: str) -> None:
        with allure.step(f"Verify page title contains {text}"):
            expect(self.page).to_have_title(re.compile(re.escape(text)))

    def assert_heading_visible(self, heading: str) -> None:
        with allure.step(f"Verify heading is visible: {heading}"):
            expect(self.page.get_by_role("heading", name=heading).first).to_be_visible()
