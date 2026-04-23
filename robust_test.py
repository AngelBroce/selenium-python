from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Configuración del Driver
driver = webdriver.Chrome()
# Definimos una espera máxima de 10 segundos
wait = WebDriverWait(driver, 10)

def ejecutar_pruebas_robustas():
    try:
        # --- CASO 1: Login Seguro ---
        print("Ejecutando Caso 1: Login Seguro...")
        driver.get("https://saucedemo.com")

        # Esperamos a que el campo de usuario sea visible antes de escribir
        user_input = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
        user_input.send_keys("standard_user")

        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait.until(EC.url_contains("inventory.html"))
        print("[OK] Caso 1 completado con éxito.")

        # --- CASO 2: Agregar al Carrito con Verificación de Clic ---
        print("Ejecutando Caso 2: Agregar producto...")
        # Esperamos a que el botón sea "clicable"
        btn_add = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
        btn_add.click()

        # Verificamos que el contador del carrito aparezca
        badge = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        print(f"[OK] Prueba exitosa: Carrito tiene {badge.text} producto(s).")

        # --- CASO 3: Validación de Error de Bloqueo ---
        print("Ejecutando Caso 3: Login fallido...")
        driver.delete_all_cookies() # Limpiamos la sesión
        driver.get("https://saucedemo.com")
        
        # Volvemos a esperar a que el campo de usuario esté visible tras recargar
        user_input = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
        user_input.send_keys("locked_out_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Esperamos a que el mensaje de error sea visible
        # (Ajuste: uso CSS Selector en lugar del inexistente By.DATA_TEST)
        error_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        
        assert "Sorry, this user has been locked out" in error_container.text
        print("[OK] Caso 3 completado con éxito.")

    except Exception as e:
        print(f"[ERROR] Error durante la ejecución: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    ejecutar_pruebas_robustas()
