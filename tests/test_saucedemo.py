from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_invalido(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.saucedemo.com/")
    
    driver.find_element(By.ID, "user-name").send_keys("usuario_incorrecto")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    error_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']")))
    # Utilizar assert nos permite fallar el test si las cosas no cuadran.
    assert "Username and password do not match" in error_element.text, "El error no fue el de credenciales nulas"

def test_login_exitoso_y_carrito(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.saucedemo.com/")
    
    # Login Exitoso Válido
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    wait.until(EC.presence_of_element_located((By.ID, "inventory_container"))) 

    # Agregar producto al carrito
    add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
    add_btn.click()

    # Validar que el botón del carrito muestre que se insertó el producto
    carrito_badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    cantidad_carrito = carrito_badge.text
    
    # [!] FORZAMOS EL ERROR PROPÓSITAMENTE CÓMO PIDIÓ EL USUARIO
    # Validando si hay 5, sabiendo realmente que hay 1. Esto estallará la foto.
    assert cantidad_carrito == "5", f"¡Ouch! Esperábamos 5, pero solo hay '{cantidad_carrito}'"

def test_demostracion_de_multiples_fallos(driver):
    # Entra a SauceDemo y forzamos un fallo muy rápido en otra funcionalidad
    driver.get("https://www.saucedemo.com/")
    assert driver.title == "Titulo Que Estalla La Prueba", "Hubo un fallo crítico validando el título de la segunda prueba."
