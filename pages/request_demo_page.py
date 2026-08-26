from __future__ import annotations

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage


class RequestDemoPage(BasePage):
    path = "/request-a-demo"
    heading = "Request a Demo"

    @property
    def first_name_input(self):
        return self.page.get_by_placeholder("First name*")

    @property
    def last_name_input(self):
        return self.page.get_by_placeholder("Last name*")

    @property
    def business_email_input(self):
        return self.page.get_by_placeholder("Business Email*")

    @property
    def company_input(self):
        return self.page.get_by_placeholder("Company name*")

    @property
    def job_title_input(self):
        return self.page.get_by_placeholder("Job title*")

    @property
    def phone_input(self):
        return self.page.get_by_placeholder("Phone number*")

    @property
    def submit_button(self):
        return self.page.locator("input[type='submit'][value='Request a Demo']")

    def assert_loaded(self) -> None:
        self.assert_heading_visible(self.heading)

    def assert_form_visible(self) -> None:
        with allure.step("Verify Request a Demo form fields are visible"):
            expect(self.page.locator("form").first).to_be_visible()
            for field in [
                self.first_name_input,
                self.last_name_input,
                self.business_email_input,
            ]:
                expect(field).to_be_visible()
            expect(self.submit_button).to_be_visible()

    def trigger_required_field_validation(self) -> None:
        with allure.step("Trigger required field validation without submitting real business data"):
            self.submit_button.click()

    def assert_required_validation_visible(self, message: str) -> None:
        with allure.step("Verify required field validation messages are visible"):
            expect(self.page.get_by_text(message).first).to_be_visible()
            expect(self.page.get_by_text("Please complete all required fields.")).to_be_visible()

    def trigger_invalid_email_validation(self, invalid_email: str) -> None:
        with allure.step("Trigger invalid email validation without completing real submission"):
            self.business_email_input.fill(invalid_email)
            self.submit_button.click()

    def assert_invalid_email_validation_visible(self, message: str) -> None:
        with allure.step("Verify invalid email validation behavior"):
            expect(self.page.get_by_text(message)).to_be_visible()
