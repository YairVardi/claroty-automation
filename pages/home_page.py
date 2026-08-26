from __future__ import annotations

from pages.base_page import BasePage


class HomePage(BasePage):
    path = "/"

    main_heading = "The AI-Powered Cyber-Physical Systems Protection Platform"

    def assert_loaded(self) -> None:
        self.assert_heading_visible(self.main_heading)
