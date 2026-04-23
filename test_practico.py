from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Configuración inicial
driver = webdriver.Chrome()
driver.implicitly_wait(10)

def ejecutar_pruebas():
    try:
        # --- CASO 1: Login Exitoso ---
        print("Ejecutando Caso 1: Login...")
        driver.get("https://saucedemo.com")
        time.sleep(2) # Pausa para ver la página de inicio
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(1) # Pausa antes de hacer clic en login
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2) # Pausa para ver el inventario (Caso 1)

        assert "inventory.html" in driver.current_url
        print("[OK] Caso 1 completado con éxito.")

        # --- CASO 2: Agregar al Carrito ---
        print("Ejecutando Caso 2: Agregar producto...")
        boton_agregar = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        boton_agregar.click()
        time.sleep(2) # Pausa para ver que se agregó al carrito (Caso 2)

        badge_carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        assert badge_carrito == "1"
        print("[OK] Caso 2 completado con éxito.")

        # --- CASO 3: Login Fallido (Usuario Bloqueado) ---
        print("Ejecutando Caso 3: Login fallido...")
        driver.delete_all_cookies() # Limpiar sesión
        driver.get("https://saucedemo.com")
        time.sleep(2) # Pausa para ver la página de inicio (Login fallido)

        driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(1) # Pausa antes de hacer clic
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2) # Pausa para ver el mensaje de error (Caso 3)

        # Usando CSS Selector para el atributo data-test (By.DATA_TEST no existe por defecto en Selenium)
        error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text 
        assert "Sorry, this user has been locked out" in error_msg
        print("[OK] Caso 3 completado con éxito.")

    except Exception as e:
        print(f"[ERROR] Error durante la ejecución: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    ejecutar_pruebas()
