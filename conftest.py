import pytest
import pytest_html
from selenium import webdriver

@pytest.fixture 
def driver():
    """Fixture del navegador""" 
    
    options = Options()
    options.add_argument("--headless") # Ejecución sin ventana (obligatorio para GitHub)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    
    driver = webdriver.Chrome()
    yield driver 
    driver.quit()
    
    # Parte de automatizacion en github
    

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