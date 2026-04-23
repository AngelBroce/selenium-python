import pytest
from selenium import webdriver
from login_page import LoginPage # Usando el modelo POM existente

@pytest.fixture
def driver():
    """Configuración del navegador"""
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login_fallido(driver):
    driver.get("https://saucedemo.com")
    login = LoginPage(driver)
    login.ingresar_credenciales("locked_out_user", "secret_sauce")
    login.click_login()
    assert "locked out" in login.obtener_error()

def test_login_exitoso(driver):
    driver.get("https://saucedemo.com")
    login = LoginPage(driver)
    login.ingresar_credenciales("standard_user", "secret_sauce")
    login.click_login()
    assert "inventory.html" in driver.current_url