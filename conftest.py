import pytest
import pytest_html
from selenium import webdriver

@pytest.fixture 
def driver():
    """Fixture del navegador""" 
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver 
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura de pantalla automática en caso de fallo""" 
    outcome = yield
    report = outcome.get_result() 
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed: 
        # Acceder al driver desde la fixture 
        driver = item.funcargs['driver']
        # Convertir la captura a base64 para el reporte HTML 
        screenshot = driver.get_screenshot_as_base64()
        html = f'<div><img src="data:image/png;base64,{screenshot}" alt="screenshot" style="width:304px;height:228px;" onclick="window.open(this.src)" align="right"/></div>'
        extras.append(pytest_html.extras.html(html))   
    report.extras = extras