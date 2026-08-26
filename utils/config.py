from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
ALLURE_RESULTS_DIR = PROJECT_ROOT / "allure-results"


@dataclass(frozen=True)
class TestConfig:
    base_url: str
    browser: str
    headless: bool
    viewport_width: int
    viewport_height: int


def _str_to_bool(value: str | bool | None, default: bool = True) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def parse_viewport(value: str | None) -> tuple[int, int]:
    raw_value = value or os.getenv("VIEWPORT", "1440x900")
    normalized = raw_value.lower().replace(",", "x").replace(" ", "")
    width, height = normalized.split("x", maxsplit=1)
    return int(width), int(height)


def load_config(browser: str | None = None, headless: str | bool | None = None, viewport: str | None = None) -> TestConfig:
    load_dotenv(PROJECT_ROOT / ".env")
    width, height = parse_viewport(viewport)
    return TestConfig(
        base_url=os.getenv("BASE_URL", "https://claroty.com").rstrip("/"),
        browser=(browser or os.getenv("BROWSER", "chromium")).lower(),
        headless=_str_to_bool(headless if headless is not None else os.getenv("HEADLESS"), default=True),
        viewport_width=width,
        viewport_height=height,
    )
