from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Generator

import pytest
from allure_commons.types import AttachmentType
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from utils.allure_helpers import attach_file_if_exists, attach_text, write_allure_environment
from utils.config import ARTIFACTS_DIR, TestConfig, load_config


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", action="store", default=None, choices=["chromium", "firefox", "webkit"])
    parser.addoption("--headed", action="store_true", default=False)
    parser.addoption("--headless", action="store", default=None, choices=["true", "false"])
    parser.addoption("--viewport", action="store", default=None, help="Viewport as WIDTHxHEIGHT, for example 1440x900")


@pytest.fixture(scope="session")
def config(pytestconfig: pytest.Config) -> TestConfig:
    headless_option = pytestconfig.getoption("--headless")
    if pytestconfig.getoption("--headed"):
        headless_option = "false"
    loaded_config = load_config(
        browser=pytestconfig.getoption("--browser"),
        headless=headless_option,
        viewport=pytestconfig.getoption("--viewport"),
    )
    write_allure_environment(loaded_config)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return loaded_config


@pytest.fixture(scope="session")
def test_data() -> dict[str, Any]:
    data_path = Path(__file__).parent / "test_data" / "test_data.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, config: TestConfig) -> Generator[Browser, None, None]:
    browser_type = getattr(playwright_instance, config.browser)
    browser = browser_type.launch(headless=config.headless)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser, config: TestConfig, request: pytest.FixtureRequest) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(
        base_url=config.base_url,
        viewport={"width": config.viewport_width, "height": config.viewport_height},
        ignore_https_errors=True,
    )
    trace_path = ARTIFACTS_DIR / f"{request.node.name}_trace.zip"
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    context.tracing.stop(path=str(trace_path) if failed else None)
    context.close()


@pytest.fixture
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    page = context.new_page()
    console_messages: list[str] = []

    def record_console(message) -> None:
        if message.type in {"error", "warning"}:
            console_messages.append(f"{message.type.upper()}: {message.text}")

    page.on("console", record_console)
    request.node.console_messages = console_messages
    yield page
    page.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = item.name.replace("/", "_").replace("::", "_")
    screenshot_path = ARTIFACTS_DIR / f"{safe_name}_screenshot.png"
    html_path = ARTIFACTS_DIR / f"{safe_name}_page.html"
    console_path = ARTIFACTS_DIR / f"{safe_name}_console.log"

    try:
        page.screenshot(path=str(screenshot_path), full_page=True)
        html_path.write_text(page.content(), encoding="utf-8")
        console_path.write_text("\n".join(getattr(item, "console_messages", [])), encoding="utf-8")
        attach_file_if_exists(screenshot_path, "Failure screenshot", AttachmentType.PNG)
        attach_file_if_exists(html_path, "Page HTML", AttachmentType.HTML)
        attach_file_if_exists(console_path, "Console errors", AttachmentType.TEXT)
        attach_text("Current URL", page.url)
    except Exception as error:
        attach_text("Artifact capture error", str(error))


@pytest.fixture(autouse=True)
def attach_trace_on_failure(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    yield
    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if failed:
        trace_path = ARTIFACTS_DIR / f"{request.node.name}_trace.zip"
        attach_file_if_exists(trace_path, "Playwright trace")
