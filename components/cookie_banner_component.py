from __future__ import annotations

import allure
from playwright.sync_api import Page


class CookieBannerComponent:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def accept_button(self):
        return self.page.get_by_role("button", name="Accept")

    @property
    def decline_button(self):
        return self.page.get_by_role("button", name="Decline")

    def handle_if_visible(self, accept: bool = False) -> None:
        with allure.step("Handle cookie banner if it appears"):
            button = self.accept_button if accept else self.decline_button
            for index in range(button.count()):
                candidate = button.nth(index)
                if candidate.is_visible():
                    candidate.click()
                    break
