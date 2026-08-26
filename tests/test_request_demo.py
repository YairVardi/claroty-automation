import allure
import pytest

from pages.request_demo_page import RequestDemoPage


@allure.epic("Claroty Public Website")
@allure.feature("Request a Demo")
@pytest.mark.smoke
@pytest.mark.form
@pytest.mark.regression
class TestRequestDemo:
    @allure.title("Request a Demo page heading and form are visible")
    @allure.story("Demo form visibility")
    @allure.description("Verifies the request demo heading and core form fields are visible.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "form")
    def test_request_demo_heading_and_form_are_visible(self, page, config) -> None:
        request_demo_page = RequestDemoPage(page, config.base_url)
        request_demo_page.open()
        request_demo_page.assert_loaded()
        request_demo_page.assert_form_visible()

    @allure.title("Required request demo fields validate without real submission")
    @allure.story("Demo form validation")
    @allure.description("Clicks the submit button with empty fields and checks client-side required-field validation.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "form", "validation")
    def test_required_form_fields_validate_without_real_submission(self, page, config, test_data) -> None:
        request_demo_page = RequestDemoPage(page, config.base_url)
        request_demo_page.open()
        request_demo_page.assert_form_visible()
        request_demo_page.trigger_required_field_validation()
        request_demo_page.assert_required_validation_visible(test_data["expected"]["required_field_message"])

    @allure.title("Invalid business email shows validation behavior")
    @allure.story("Demo form validation")
    @allure.description("Fills only an invalid email value and verifies the supported email-format validation message.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "form", "email-validation")
    def test_invalid_email_input_displays_validation_behavior(self, page, config, test_data) -> None:
        request_demo_page = RequestDemoPage(page, config.base_url)
        request_demo_page.open()
        request_demo_page.assert_form_visible()
        request_demo_page.trigger_invalid_email_validation(test_data["invalid_email"])
        request_demo_page.assert_invalid_email_validation_visible(test_data["expected"]["invalid_email_message"])
