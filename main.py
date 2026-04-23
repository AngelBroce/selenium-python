from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("Inicializando navegador...")
driver = webdriver.Chrome()

try:
    print("Abriendo https://www.saucedemo.com/ ...")
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    # =============== FASE 1: LOGIN INVÁLIDO ===============
    print("\n--- FASE 1: PROBANDO LOGIN INVÁLIDO ---")
    driver.find_element(By.ID, "user-name").send_keys("usuario_incorrecto")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Validar mensaje de error
    error_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']")))
    print(f" [Exito!] Mensaje de error interceptado: '{error_element.text}'")

    # Limpiar campos o simplemente recargar la página para el test exitoso
    driver.refresh()

    # =============== FASE 2: LOGIN EXITOSO ===============
    print("\n--- FASE 2: LOGIN CORRECTO Y CARRITO ---")
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Validación de inventario
    wait.until(EC.presence_of_element_located((By.ID, "inventory_container"))) 
    print(" [Exito!] Login validado correctamente. Estamos en el inventario.")

    # Agregar producto al carrito
    print("Añadiendo mochila al carrito...")
    add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
    add_btn.click()

    # Validar que el botón del carrito muestre 1
    carrito_badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    cantidad_carrito = carrito_badge.text
    
    assert cantidad_carrito == "1", f"Error: Se esperaba 1 producto en el carrito, pero se encontraron {cantidad_carrito}"
    print(f" [Exito!] Prueba completada! El carrito tiene: {cantidad_carrito} producto(s).")

except Exception as e:
    print(f" [Fallo] La prueba se detuvo: {e}")
finally:
    # Cerrar navegador
    print("Cerrando navegador...")
    driver.quit()
