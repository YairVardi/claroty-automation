# Claroty UI Automation

Production-style UI automation for `https://claroty.com` using Python, Playwright synchronous API, pytest, Page Object Model, Allure, and Jenkins.

## Project Setup

```bash
cd claroty-automation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python -m playwright install chromium firefox webkit
```

Linux agents may also need browser system libraries:

```bash
python -m playwright install --with-deps chromium
```

## Local Execution

Run the smoke suite with the required reports:

```bash
pytest -m smoke --browser chromium --alluredir=allure-results --clean-alluredir --junitxml=artifacts/junit.xml
```

Run all tests:

```bash
pytest --alluredir=allure-results --clean-alluredir --junitxml=artifacts/junit.xml
```

Run headed mode:

```bash
pytest -m smoke --browser chromium --headed --alluredir=allure-results --clean-alluredir --junitxml=artifacts/junit.xml
```

Run a specific browser:

```bash
pytest -m smoke --browser firefox --alluredir=allure-results --clean-alluredir --junitxml=artifacts/junit.xml
pytest -m smoke --browser webkit --alluredir=allure-results --clean-alluredir --junitxml=artifacts/junit.xml
```

Override configuration with environment variables:

```bash
BASE_URL=https://claroty.com BROWSER=chromium HEADLESS=true VIEWPORT=1440x900 pytest -m smoke
```

## Allure Reports

Raw Allure results are written to `allure-results`. Open the local report with:

```bash
allure serve allure-results
```

The report includes base URL, browser, Python version, operating system, Jenkins build number when available, and Git commit when available.

## IntelliJ or PyCharm

1. Open `claroty-automation` as the project root.
2. Go to `Settings > Project > Python Interpreter`.
3. Choose `Add Interpreter > Existing`.
4. Select `claroty-automation/.venv/bin/python`.
5. Configure pytest as the test runner under `Settings > Tools > Python Integrated Tools`.

## Jenkins

Create a Pipeline job from source control:

1. Install Jenkins plugins: Pipeline, JUnit, and Allure.
2. Install Allure Commandline on the Jenkins controller/agent.
3. Configure Allure Commandline under `Manage Jenkins > Tools > Allure Commandline`.
4. Create a new Pipeline job.
5. Select `Pipeline script from SCM`.
6. Point SCM to this repository and use `Jenkinsfile`.

The Jenkinsfile exposes these parameters:

| Parameter | Default | Description |
| --- | --- | --- |
| `BASE_URL` | `https://claroty.com` | Target site |
| `BROWSER` | `chromium` | `chromium`, `firefox`, or `webkit` |
| `TEST_MARKER` | `smoke` | pytest marker expression |
| `HEADLESS` | `true` | headless or headed execution |

Jenkins uses `.venv`, cleans `allure-results` and `artifacts`, runs the selected marker and browser, publishes JUnit and Allure in `post { always { ... } }`, archives failure artifacts, and fails the build when pytest fails. Tests are not parallelized by default to avoid unnecessary load against the public website.

## Troubleshooting

Missing browser binaries:

```bash
python -m playwright install chromium firefox webkit
```

Linux dependency failures:

```bash
python -m playwright install --with-deps chromium
```

If system package installation is restricted on a Jenkins agent, preinstall the packages listed by Playwright or use an agent image that already supports Playwright browsers.

## Implemented Coverage

- Homepage load, title, main heading, header, and footer.
- Header navigation and Request a Demo CTA.
- Request a Demo form visibility, required-field validation, and invalid email validation without real submission.
- Search flow using the safe term `xDome`.
- Careers page heading and current openings link.
- Footer Terms & Conditions and Privacy Policy links.
- Mobile navigation menu with a mobile viewport.
- Consistent cookie banner handling when it appears.
