from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_robust_flujo_completo(driver):
    wait = WebDriverWait(driver, 10)

    # Login
    driver.get("https://saucedemo.com")

    user = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    user.send_keys("standard_user")

    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Validar login
    wait.until(EC.url_contains("inventory.html"))
    assert "inventory.html" in driver.current_url

    # Agregar producto
    btn_add = wait.until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    )
    btn_add.click()

    # Validar carrito
    badge = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert badge.text == "1"


def test_login_fallido_robusto(driver):
    wait = WebDriverWait(driver, 10)

    driver.get("https://saucedemo.com")

    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    error = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )

    assert "locked out" in error.text