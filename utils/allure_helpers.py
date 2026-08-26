from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path

import allure
from allure_commons.types import AttachmentType

from utils.config import ALLURE_RESULTS_DIR, TestConfig


def attach_text(name: str, value: str) -> None:
    allure.attach(value, name=name, attachment_type=AttachmentType.TEXT)


def attach_file_if_exists(path: Path, name: str, attachment_type: AttachmentType | None = None) -> None:
    if not path.exists():
        return
    if attachment_type is None:
        allure.attach.file(str(path), name=name)
    else:
        allure.attach.file(str(path), name=name, attachment_type=attachment_type)


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unavailable"


def write_allure_environment(config: TestConfig) -> None:
    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    values = {
        "Base URL": config.base_url,
        "Browser": config.browser,
        "Python version": sys.version.split()[0],
        "Operating system": f"{platform.system()} {platform.release()}",
        "Jenkins build number": platform.os.environ.get("BUILD_NUMBER", "local"),
        "Git commit": _git_commit(),
    }
    content = "\n".join(f"{key}={value}" for key, value in values.items())
    (ALLURE_RESULTS_DIR / "environment.properties").write_text(content, encoding="utf-8")
