import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Fixture del navegador
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")  # necesario para GitHub Actions
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# Hook para capturas en fallos
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)

        if driver:
            screenshot = driver.get_screenshot_as_base64()
            html = f'<div><img src="data:image/png;base64,{screenshot}" style="width:300px;" onclick="window.open(this.src)" /></div>'

            extra = getattr(report, "extra", [])
            extra.append(pytest_html.extras.html(html))
            report.extra = extra