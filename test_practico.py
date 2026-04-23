from selenium.webdriver.common.by import By

def test_login_exitoso(driver):
    driver.get("https://saucedemo.com")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    assert "inventory.html" in driver.current_url


def test_agregar_carrito(driver):
    driver.get("https://saucedemo.com")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert badge == "1"


def test_login_fallido(driver):
    driver.get("https://saucedemo.com")

    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "locked out" in error